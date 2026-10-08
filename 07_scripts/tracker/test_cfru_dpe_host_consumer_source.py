#!/usr/bin/env python3
"""#707 immutable extraction, side-effect inventory, scope and executable isolation."""
import hashlib
from pathlib import Path
import re
import subprocess
import unittest
from unittest.mock import patch
import run_cfru_dpe_host_consumer_mock_tests as host

ALLOWED = {
    '07_scripts/tracker/run_cfru_dpe_host_consumer_mock_tests.py',
    '07_scripts/tracker/tests/cfru_dpe_host_consumer_mock.lua',
    '07_scripts/tracker/test_cfru_dpe_host_consumer_source.py',
    'docs/tracker/T5_HOST_CONSUMER_SANDBOX.md',
}
# Independent reviewed exact boundaries; end excludes following declaration/comments.
REVIEWED = {
    'Program.readNewPokemon': (888,1015,'a3e31f4f1aac4e0bbd97c94b6e9c9de6e922f22b98f4b7d57681dff12c00398c'),
    'Program.updatePokemonTeams': (827,886,'c3a5a646deebcf9e1fcf628c3cdf2442f56aac53e08b595a425a223c0fc6894f'),
    'Program.validPokemonData': (1432,1453,'8122baf91078290a75fda939b50c8d1b71566e10193d0b1b39ca6a2a78d359ff'),
    'Battle.inActiveBattle': (112,114,'6af0d214287cab7c975c5e060b0e2cc66f44da2b761b0eba9cae134619f081ee'),
    'Battle.getViewedPokemon': (257,267,'1fa621dbc5017b96dedba1145603d37eea1aaf656836ea76ed9416091107c8ce'),
    'Battle.updateViewSlots': (269,318,'fed774b25386214c09e4c31a4a01c63ea3d75fe10e0465bab346785890760b17'),
    'Battle.beginNewBattle': (739,810,'dc40497a14d8446e6fb4f29ded71fd3314a58c14d331ade6d7e8e1d636fd853d'),
    'TrackerAPI.getPlayerPokemon': (28,33,'dd201768d4c7c4d64c498eca1cc41d2aadbbb59561d1ec6ce76bcb7cd8ccf2f6'),
    'TrackerAPI.getEnemyPokemon': (38,43,'e4713b917d874a69b29fe248519e050cee1834fa642f0d32d9475568625bdd3f'),
    'TrackerAPI.getActiveBattlePokemon': (47,59,'fd683e9991d7740bed5e0fa1d9ec64a3b9e6ec351a75f84df2163dca7f4ceaa0'),
    'Tracker.getPokemon': (105,140,'c2f757beb7c2e438b69c5ea4aebb617dedf72b72313d507c35dfdbb870960351'),
    'Tracker.saveData': (612,615,'2175f08b78820b3c447e80e80d875c43bc8f45e6fc95b515ef02f9924ed0f2da'),
    'Tracker.loadData': (632,676,'34296c0cea44fafef104e714e67270e88a0224ff18bb1323d897b6781ed7dd8e'),
    'Tracker.verifyDataForPlayer': (680,697,'6d3f4cc1b32d07bba467c1955022916bbd9a965f5c006e269e2851a9253136dc'),
    'DataHelper.buildTrackerScreenDisplay': (124,412,'9593b7625c8b38817194c4ab034eaf19397c7650a7845f758bc572f9742e679e'),
}


class HostConsumerSourceTests(unittest.TestCase):
    def test_all_definitions_exact_reviewed_bytes_and_boundaries(self):
        selected, proof = host.definitions()
        self.assertEqual(set(selected),set(REVIEWED))
        for name,(first,last,digest) in REVIEWED.items():
            self.assertEqual((proof[name]['first'],proof[name]['last']),(first,last),name)
            self.assertEqual(hashlib.sha256(selected[name].encode()).hexdigest(),digest,name)

    def test_nested_blocks_comments_strings_and_no_adjacent_execution(self):
        text = '''dangerousLauncher()
function Probe.selected()
 local s="function end if" -- end function
 --[=[ end do function ]=]
 local long=[==[ end until ]==]
 for i=1,2 do if i then while false do end elseif false then do end end end
 repeat local f=function() return 1 end until true
end
unapprovedNextCall()
'''
        body,first,last=host.extract(text,'Probe.selected')
        self.assertEqual((first,last),(2,8))
        self.assertTrue(body.endswith('end'))
        self.assertNotIn('dangerousLauncher',body)
        self.assertNotIn('unapprovedNextCall',body)

    def test_missing_duplicate_unbalanced_definitions_rejected(self):
        for text in ('function Probe.other() end',
                     'function Probe.selected() end function Probe.selected() end',
                     'function Probe.selected() if true then end',
                     'function Probe.selected() repeat end end'):
            with self.assertRaises(ValueError): host.extract(text,'Probe.selected')

    def test_pin_and_content_drift_fail_before_lua(self):
        original = host.git
        def wrong_pin(*args,**kwargs):
            if args==('rev-parse','HEAD'): return b'0'*40+b'\n'
            return original(*args,**kwargs)
        with patch.object(host,'git',side_effect=wrong_pin):
            with self.assertRaisesRegex(ValueError,'approved pin'): host.public_sources()
        original_read=Path.read_bytes
        def drift(path):
            raw=original_read(path)
            return raw+b'\n--synthetic drift' if path.name=='Program.lua' else raw
        with patch.object(Path,'read_bytes',drift):
            with self.assertRaisesRegex(ValueError,'pinned blob'): host.public_sources()

    def test_exact_four_new_paths_all_gitlinks_and_component_status(self):
        rows=host.git('diff','--name-only',host.BASE).decode().splitlines()
        self.assertTrue(set(rows)<=ALLOWED,rows)
        for p in ALLOWED:
            result=subprocess.run(['git','cat-file','-e',host.BASE+':'+p],cwd=host.ROOT,capture_output=True)
            self.assertNotEqual(result.returncode,0,'Authorized path must be new: '+p)
        def links(ref):
            return [r for r in host.git('ls-tree','-r',ref).splitlines() if r.startswith(b'160000 ')]
        self.assertEqual(len(links('HEAD')),10)
        self.assertEqual(links('HEAD'),links(host.BASE))
        self.assertEqual(links('HEAD'),links('3bdfe9919afc0b7bea55c79f37285e832be495c3'))
        self.assertFalse(host.git('diff','--name-only','--','02_external').strip())
        for row in links('HEAD'):
            path=row.split(b'\t')[1].decode(); pin=row.split()[2].decode()
            checkout=host.ROOT/path
            self.assertEqual(host.git('rev-parse','HEAD',cwd=checkout).decode().strip(),pin)
            self.assertEqual(host.git('status','--porcelain','--untracked-files=no',cwd=checkout),b'')

    def test_not_run_consumer_source_witnesses(self):
        texts=host.public_sources()
        draw,first,last=host.extract(texts['screens/TrackerScreen.lua'],'TrackerScreen.drawScreen')
        self.assertEqual((first,last),(1102,1125))
        for witness in ('DataHelper.buildTrackerScreenDisplay','drawPokemonInfoArea','drawStatsArea','drawCarouselArea','drawMovesArea'):
            self.assertIn(witness,draw)
        details=texts['screens/BattleDetailsScreen.lua']
        for witness in ('function SCREEN.updateData','Memory.readdword(GameSettings.gBattleMons',
                        'Memory.readdword(GameSettings.gStatuses3','Memory.readword(GameSettings.gSideStatuses',
                        'Memory.readbyte(GameSettings.gBattleTerrain'):
            self.assertIn(witness,details)
        self.assertIn('local monLvIndex = pokemonID * 1000 + level',texts['Tracker.lua'])
        begin,_,_=host.extract(texts['Battle.lua'],'Battle.beginNewBattle')
        self.assertLess(begin.index('GameOverScreen.createTempSaveState()'),begin.index('CustomCode.afterBattleBegins()'))

    def test_harness_has_no_extra_modules_or_normal_startup(self):
        runner=(host.ROOT/'07_scripts/tracker/run_cfru_dpe_host_consumer_mock_tests.py').read_text()
        harness=(host.ROOT/'07_scripts/tracker/tests/cfru_dpe_host_consumer_mock.lua').read_text()
        self.assertNotIn('Main.lua',runner)
        self.assertNotRegex(runner,r'\b(?:glob|rglob|walk)\(')
        stream=[token for token,_,_ in host.tokens(harness)]
        self.assertFalse(any(stream[i] in {'dofile','require','loadfile'} and stream[i+1]=='(' for i in range(len(stream)-1)))
        self.assertIn("trustedLoad(body,'@PIN/'..name,'t',env)",harness)
        self.assertIn('No execution coverage:',harness)
        self.assertIn("production=DENIED",harness)
        self.assertIn("liveConfidence=UNKNOWN",harness)


if __name__=='__main__': unittest.main()
