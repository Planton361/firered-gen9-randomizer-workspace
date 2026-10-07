-- SHA-256 for public source text only. Portable arithmetic, Lua 5.1 / 5.4.
-- No emulator API, native bit operators, executable inputs or dependencies.
local MOD = 4294967296
local floor = math.floor
local xor4, and4 = {}, {}
for a = 0, 15 do
    xor4[a], and4[a] = {}, {}
    for b = 0, 15 do
        local x, y, p, av, bv = 0, 0, 1, a, b
        for _ = 1, 4 do
            local aa, bb = av % 2, bv % 2
            if aa ~= bb then x = x + p end
            if aa == 1 and bb == 1 then y = y + p end
            av, bv, p = floor(av / 2), floor(bv / 2), p * 2
        end
        xor4[a][b], and4[a][b] = x, y
    end
end
local function bitop(a, b, lookup)
    local result, p = 0, 1
    for _ = 1, 8 do
        result = result + lookup[a % 16][b % 16] * p
        a, b, p = floor(a / 16), floor(b / 16), p * 16
    end
    return result
end
local function xor(a, b) return bitop(a, b, xor4) end
local function band(a, b) return bitop(a, b, and4) end
local function ror(a, n)
    local p = 2 ^ n
    return floor(a / p) + (a % p) * (MOD / p)
end
local function mix(a, b, c) return xor(xor(a, b), c) end
local K = {
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2,
}
local function wordBytes(n)
    return string.char(floor(n / 16777216) % 256, floor(n / 65536) % 256,
        floor(n / 256) % 256, n % 256)
end
return function(input)
    assert(type(input) == "string", "public source text required")
    local bits = #input * 8
    local data = input .. string.char(128) .. string.rep(string.char(0), (55 - #input) % 64)
        .. wordBytes(floor(bits / MOD)) .. wordBytes(bits % MOD)
    local h = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19}
    for offset = 1, #data, 64 do
        local w = {}
        for i = 0, 15 do
            local a,b,c,d = string.byte(data, offset + i * 4, offset + i * 4 + 3)
            w[i] = a * 16777216 + b * 65536 + c * 256 + d
        end
        for i = 16, 63 do
            local x, y = w[i-15], w[i-2]
            w[i] = (w[i-16] + mix(ror(x,7),ror(x,18),floor(x/8)) + w[i-7]
                + mix(ror(y,17),ror(y,19),floor(y/1024))) % MOD
        end
        local a,b,c,d,e,f,g,j = h[1],h[2],h[3],h[4],h[5],h[6],h[7],h[8]
        for i = 0, 63 do
            local t1 = (j + mix(ror(e,6),ror(e,11),ror(e,25))
                + xor(band(e,f),band(MOD-1-e,g)) + K[i+1] + w[i]) % MOD
            local t2 = (mix(ror(a,2),ror(a,13),ror(a,22))
                + mix(band(a,b),band(a,c),band(b,c))) % MOD
            a,b,c,d,e,f,g,j = (t1+t2)%MOD,a,b,c,(d+t1)%MOD,e,f,g
        end
        local values = {a,b,c,d,e,f,g,j}
        for i = 1, 8 do h[i] = (h[i] + values[i]) % MOD end
    end
    local result = {}
    for i = 1, 8 do result[i] = string.format("%08x",h[i]) end
    return table.concat(result)
end
