# UPR FVX Source Build Smoke Test

## Datum

2026-05-11

## Quelle

- Fork: Planton361/universal-pokemon-randomizer-fvx
- Upstream: upr-fvx/universal-pokemon-randomizer-fvx
- Submodule: `02_external/upr-fvx`
- Branch: compat/firered-gen9-cfru-dpe
- Commit: e0788edc6529c2605f201996e4807ff30165354c

## Build-Voraussetzung

- JDK 25: `/usr/lib/jvm/java-25-openjdk`
- Gradle Wrapper: `02_external/upr-fvx/gradlew`

## Build-Befehl

```sh
JAVA_HOME=/usr/lib/jvm/java-25-openjdk ./gradlew :random:jar
```

## JAR

```text
cdda8c6c645f5c6f730f37b17dec521e2606a480c56cc8ff83227cc86b8abcd0  02_external/upr-fvx/random/build/libs/UPR-FVX.jar
```

## Start-Befehl

```sh
JAVA_HOME=/usr/lib/jvm/java-25-openjdk /usr/lib/jvm/java-25-openjdk/bin/java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar
```

## Ergebnis

- Build erfolgreich: ja
- GUI gestartet: ja
- ROM geladen: nein
- Hinweise: UPR-FVX wurde aus Source gebaut und die GUI wurde gestartet. Keine ROM geladen.
