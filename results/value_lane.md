# Value arithmetic as the cipher

Registration: `results/value_lane_registration.md`. 24 rules × 10,621 keys (2,905 phrase keys and 3,000 prime-stream variants in pass 1, 4,716 word and text keys in pass 2) × 2 F × 55 pages = **28,039,440 decodes**; z against 400 random keys per (page, rule, F). Largest z 7.05; largest null z over every null draw 4.76.

## Controls (English at page length under the rule, soft 0.81, a random book key; decoded over the 7,621 book keys)

| rule | F | planted key | z | rank | top is planted | rune accuracy | pass |
|---|---|---|---|---|---|---|---|
| prime p+k mod 29 | False | ('phrase-4-rev', 'ALL THAT YOU OWN ʳ') | 14.5 | 1 | True | 0.91 | yes |
| totient p-k mod 110 | True | ('phrase-4-rev', 'IT IS THE DUTY ʳ') | 14.7 | 1 | True | 0.83 | yes |
| prime k-p mod 113 | False | ('phrase-4', 'EVERY PILGRIM TO SEEK') | 14.6 | 1 | True | 0.85 | yes |
| totient p*k mod 29 | True | ('phrase-2', 'BELIEVE WE') | 14.6 | 1 | True | 0.89 | yes |
| prime p*k mod 110 | False | ('phrase-3', 'AFTER A LONG') | 16.3 | 1 | True | 0.84 | yes |
| totient p+k mod 113 | True | ('phrase-4-rev', 'WE FOLLOW DOGMA SO ʳ') | 16.1 | 1 | True | 0.83 | yes |

Controls passing: 6 of 6.

## Rows at z ≥ 4.5 (top 25)

| page | rule | F | key | z (corrected) | raw z | rank | transliteration |
|---|---|---|---|---|---|---|---|
| LP2-52 | totient p*k mod 113 | True | ('phrase-2-rev', 'SHOULD BE ʳ') | 7.05 | 5.94 | 1 | SFHFWOTNFTTHNGYNGMNIAEGNGWNGFINIARRMIPFRBRCWEFFDFWSIAUYDFURA |
| LP2-13 | prime p*k mod 29 | True | prime p s=50 | 6.10 | 5.69 | 1 | IHFFOEWLJSIASEATULXEEAGELHTHIYETHEIEFEOIAHSSFGETHRIFWJJWHCWN |
| LP2-13 | prime p*k mod 29 | True | ('primes', 'p[n+50]') | 6.10 | 5.69 | 1 | IHFFOEWLJSIASEATULXEEAGELHTHIYETHEIEFEOIAHSSFGETHRIFWJJWHCWN |
| LP2-13 | prime p*k mod 29 | True | prime p s=49 | 5.76 | 5.40 | 1 | FIANFOEWLJSIASEATULXEEAGELHTHIYETHEIEFEOIAHSSFGETHRIFWJJWHCW |
| LP2-13 | prime p*k mod 29 | True | ('primes', 'p[n+49]') | 5.76 | 5.40 | 1 | FIANFOEWLJSIASEATULXEEAGELHTHIYETHEIEFEOIAHSSFGETHRIFWJJWHCW |
| LP2-43 | prime p+k mod 110 | True | ('vigenere-word', 'HAUE') | 5.71 | 5.34 | 1 | PSOBYFUSEEAILIBAFTFURUIAWPOFIAANCSILNGEOYFYFSTNGCEONCSLDOLNU |
| LP2-31 | totient p+k mod 29 | False | prime p+1 s=198 | 5.55 | 5.55 | 1 | IWOTHUELIAFFYTWFUAGWAGFLEAYFOCFREWROECYPUOTHUWPYJULILYTHOIJJ |
| LP2-44 | prime p*k mod 110 | True | ('vigenere-word-rev', 'IRRITATEDʳ') | 5.53 | -0.22 | 1 | CHJHFFFFFXFHIAFJTHFHFPEALCXFFEMFCYFEFDRFFLYDOEFEABFTAXNHLEFO |
| LP2-42 | totient k-p mod 29 | True | prime p-1 s=475 | 5.43 | 5.43 | 1 | NOEOSRNGTHEYHHONNGUJTCOAYYIXYIHGEAFIAUFTEOIPXSIARWIEAITHEACL |
| LP2-48 | prime p*k mod 110 | True | ('phrase-2', 'THE MASTER') | 5.40 | 0.75 | 1 | WTHEAHYJPFFMUIANAUFFFNGSYWWIFOOAUCTHLFIODFEAFENGIXSEOFFFREOE |
| LP2-13 | prime p*k mod 29 | True | ('self running key', 'plaintext@2772') | 5.40 | 2.73 | 1 | OTFEOGEPPFOPRTFYCIASACFEAOEROEIAHFCFFCTLLJEIAHYJAYOILXJTHLFJ |
| LP2-13 | prime p*k mod 29 | True | ('self running key', 'plaintext@2770') | 5.36 | 2.70 | 1 | WIAFJUYWPFOPRTFYCIASACFEAOEROEIAHFCFFCTLLJEIAHYJAYOILXJTHLFJ |
| LP2-11 | totient p*k mod 110 | True | prime p s=285 | 5.25 | 3.50 | 1 | WFTHFFSNGRTHOFFWWFENGIFFFNEWFTHAPOEIPUTFUPLLPTFAEFLTHLTHFIFE |
| LP2-04 | prime p+k mod 29 | True | prime p-1 s=589 | 5.23 | 5.23 | 1 | EPIAHEASRIJJGEAECNGNSIGWTHWGIXRRTHATHGFNGEAPLFFCLFEAESUERRTH |
| LP2-13 | prime p*k mod 29 | True | ('self running key', 'plaintext@2771') | 5.21 | 2.57 | 1 | IEONEOGEPPFOPRTFYCIASACFEAOEROEIAHFCFFCTLLJEIAHYJAYOILXJTHLF |
| LP2-00 | totient k-p mod 113 | True | ('phrase-2-rev', 'OR CHANGE ʳ') | 5.19 | 4.97 | 1 | HAIFIPRFFCIXBIFLPFEGFSOEONGMEACXMENFEFJURJEOEAFFEAFTRFFEGSEA |
| LP2-42 | prime k-p mod 29 | True | prime p-1 s=475 | 5.19 | 5.19 | 1 | NOEOSRNGTHEYHHONNGUJTCOAYYIXYIHGEAFIAUFTEOIPXSIARWIEAITHEACL |
| LP2-26 | totient k-p mod 113 | True | ('self running key', 'plaintext@455') | 5.18 | 4.98 | 1 | EOFNBOWFFFNGLMNAJNRFOIJUISXWFEFEFNFDEASXYWLIUEAUTGTXRAFBLMEA |
| LP2-41 | totient k-p mod 110 | True | prime p+1 s=302 | 5.17 | 5.08 | 1 | HIACGHFDCNGPJUIFUHOEBNNAPESFXFASIAMUEOIOFATUFNPEAHNGLEOLGWUF |
| LP2-13 | prime p*k mod 29 | True | ('self running key', 'plaintext@2769') | 5.17 | 2.54 | 1 | FYNJUYWPFOPRTFYCIASACFEAOEROEIAHFCFFCTLLJEIAHYJAYOILXJTHLFJT |
| LP2-43 | totient k-p mod 113 | True | ('phrase-3', 'WHAT WE HAVE') | 5.16 | 3.58 | 1 | RENENRPNFNFFPRBHOEEOHLFMGTLSHPFEXETFTOHHNFEOMATNMFRFLXOLIAEA |
| LP2-11 | totient p*k mod 110 | True | prime p s=286 | 5.14 | 3.42 | 1 | FDFFCWJTHWAEFBLTCFFNGIFFFNEWFTHAPOEIPUTFUPLLPTFAEFLTHLTHFIFE |
| LP2-09 | totient p-k mod 113 | True | ('phrase-2', 'FIND THE') | 5.14 | 4.85 | 1 | FEOERYHNGSEOXOUFMUSTOESAWBIILBOWFTHOELXWFJSRDOFCSLOIPXALICRJ |
| LP2-04 | totient p*k mod 113 | True | prime p s=780 | 5.14 | 4.40 | 1 | ATORSHRLFEFLFENIFWEOWFTHBAUFIHYICAESIUTYCTHOEOAEFCFNGOFGNTIA |
| LP2-13 | prime p-k mod 110 | True | prime p-1 s=491 | 5.11 | 5.15 | 1 | ELDCRTHUIURCWEAGNWGGFIROGTOLAYOEWGYSWEONGLXAWROIANGSTNUWTHWN |

## Candidates

- {'rule': 'totient p*k mod 113', 'F': True, 'key': "('phrase-2-rev', 'SHOULD BE ʳ')", 'z': 7.054138420035456, 'zraw': 5.936619161489563, 'rank': 1, 'tr': 'SFHFWOTNFTTHNGYNGMNIAEGNGWNGFINIARRMIPFRBRCWEFFDFWSIAUYDFURAOLTHFGIAFLUWOEOSPD', 'page': 'LP2-52'}
- {'rule': 'prime p*k mod 29', 'F': True, 'key': 'prime p s=50', 'z': 6.100808704262534, 'zraw': 5.6869702431801334, 'rank': 1, 'tr': 'IHFFOEWLJSIASEATULXEEAGELHTHIYETHEIEFEOIAHSSFGETHRIFWJJWHCWNSGHALWHIATHNEHENGFETHF', 'page': 'LP2-13'}
- {'rule': 'prime p*k mod 29', 'F': True, 'key': "('primes', 'p[n+50]')", 'z': 6.100808704262534, 'zraw': 5.6869702431801334, 'rank': 1, 'tr': 'IHFFOEWLJSIASEATULXEEAGELHTHIYETHEIEFEOIAHSSFGETHRIFWJJWHCWNSGHALWHIATHNEHENGFETHF', 'page': 'LP2-13'}

- V1 controls 6/6: **holds**.
- V2 no candidate: **fails**.

Reading: null. 28,039,440 corrected decodes in two passes (the 2,905 phrase keys and 3,000 prime-stream variants, then the 4,716 word and text keys, the second pass added after the first had been written with one key set where the registration named both); 182 rows at z ≥ 4.5; the two rows that meet the three mechanical conditions (the third listed is the same prime stream under its phase-3 label) are unreadable, 5-gram z +4.2 and +1.7 against +51 for English at page length, and one falls to 5.1 on a fresh null draw (`results/value_lane_candidates.md`). V2's merge flag omits the registered readability clause; under the registered rule there is no candidate. [stated — the tables and the candidates note]

Runtime, longest shard: 0.8 h on 16 shards.
