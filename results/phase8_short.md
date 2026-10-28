# Phase 8 (LCG seeds, position multipliers) on the nine short pages: 5-gram rescoring (README §37)

Rule: z_uni >= 3.5 and z_5 >= 6.0 (5-gram over 400 random keystreams through the same decoder) and readable; controls planted at short lengths.

## Controls

| n | set | key | F | z_uni | z_5 | rank | pass |
|---|---|---|---|---|---|---|---|
| 92 | lcg(a=1033,c=0,m=3301) add | seed=3029 | False | 6.0 | 32.9 | 1 | yes |
| 137 | lcg(a=3,c=0,m=3301) add | seed=370 | False | 7.6 | 39.8 | 1 | yes |
| 159 | lcg(a=7,c=1,m=3301) add | seed=1994 | False | 8.5 | 40.1 | 1 | yes |
| 196 | lcg(a=7,c=1,m=3301) beaufort | seed=301 | False | 10.4 | 51.5 | 1 | yes |
| 92 | lcg(a=2,c=24,m=29) add | seed=1 | False | 6.5 | 31.8 | 1 | yes |
| 137 | lcg(a=3301,c=29,m=1033) add skip2 | seed=269 | False | 6.3 | 25.7 | 1 | yes |
| 159 | word keys × position multiplier | m=(22i+18)%28+1 | False | 8.3 | 37.8 | 1 | yes |
| 196 | lcg(a=1033,c=0,m=3301) add | seed=2475 | True | 12.9 | 31.7 | 1 | yes |
| 92 | lcg(a=3,c=0,m=3301) add | seed=1905 | True | 6.1 | 23.7 | 1 | yes |
| 137 | lcg(a=7,c=1,m=3301) add | seed=1911 | True | 8.9 | 39.6 | 1 | yes |
| 159 | lcg(a=7,c=1,m=3301) beaufort | seed=1960 | True | 10.3 | 36.4 | 1 | yes |
| 196 | lcg(a=2,c=24,m=29) add | seed=0 | True | 11.8 | 47.4 | 1 | yes |
| 92 | lcg(a=3301,c=29,m=1033) add skip2 | seed=111 | True | 6.7 | 35.2 | 1 | yes |
| 137 | word keys × position multiplier | m=(25i+25)%28+1 | True | 9.3 | 31.1 | 1 | yes |
| 159 | lcg(a=1033,c=0,m=3301) add | seed=562 | False | 8.2 | 38.2 | 2 | no |
| 196 | lcg(a=3,c=0,m=3301) add | seed=412 | False | 10.3 | 45.9 | 1 | yes |

Controls passing: 15 of 16.

## Best cell per page

| page | set | F | family | key | z_uni | z_5 | transliteration |
|---|---|---|---|---|---|---|---|
| LP2-06 | lcg(a=3,c=0,m=3301) add | False | lcg(3,0,3301) | seed=100 | 3.82 | 0.1 | RRPEMANGNDIEOSGTBPONREANGEBRNONTSGTHGRLHYRFYAOXGEE |
| LP2-14 | word keys × position multiplier | True | word×schedule FIRFUMFERENFE | m=(24i+19)%28+1 | 3.46 | -2.5 | ALFECWTHNUJPBUNTHIUHORLNLOHAYRREOTHBWPAEIAIEAIALET |
| LP2-15 | word keys × position multiplier | True | word×schedule FIRFUMFERENFE | m=(4i+6)%28+1 | 4.45 | -1.4 | FSOUUIEAPSRAJMNGWBEPFEAPIMAMLEFTSRTOOAYERPBIAAMPTG |
| LP2-22 | lcg(a=3,c=0,m=3301) add | False | lcg(3,0,3301) | seed=1676 | 3.81 | -1.1 | CALYPWNSRMANSLDCGWTMIEAIATGHETOEMPRBWOGYAMPIANGMPA |
| LP2-32 | lcg(a=1033,c=0,m=3301) add | True | lcg(1033,0,3301) | seed=2070 | 3.37 | 2.0 | NEASNGRHNSFHRTHRRSEOENTOEYISNGETWPTHFLITHBONEEARDU |
| LP2-49 | lcg(a=1033,c=0,m=3301) add | True | lcg(1033,0,3301) | seed=2644 | 3.53 | -1.8 | WANFSSCORIUHREEABLCHGUOTHMXUNSTHARRIRHUREAGSBMOJMW |
| LP2-51 | lcg(a=3,c=0,m=3301) add | True | lcg(3,0,3301) | seed=2637 | 3.68 | -0.9 | OMLTWEOPYBYLHTHSECTNGDPFAWEWSDUONHGXRRCPUAURDEAEEB |
| LP2-53 | lcg(a=1033,c=0,m=3301) add | True | lcg(1033,0,3301) | seed=3066 | 3.48 | -0.1 | URAELXDHUHCRCUDIAEFDXEADDEEAESUXHBOCUREENDNWGNLOTH |
| LP2-55 | word keys × position multiplier | True | word×schedule DIVINITY | m=(13i+26)%28+1 | 3.42 | -2.0 | UDIFIYEPTHEAPYXLFOOCNOISXNGFRJINDLOWGYTHTJLOFRLUUI |

## Candidates

None.

Largest z_uni 4.45; largest z_5 2.03.

