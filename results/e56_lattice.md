# The E56w+n decoder on a word-lattice plaintext (known keys)

Registration: `results/e56_lattice_registration.md`. Beam 8 key-offset states; null 2000 random keystreams per (page, F).

## Power: 30 E56w+n plants (Bunyan words, 262 runes, library keys, signs and F cycled)

| decoder | recovered (rank 1, z ≥ 6) | median z | median rune accuracy |
|---|---|---|---|
| plain | 0 / 30 | 2.3 | 0.19 |
| free-null | 22 / 30 | 13.0 | 0.85 |
| e56 | 30 / 30 | 82.7 | 0.94 |

Fillers planted (median) 28, placed by the decoder 28, share found 0.93; echoes planted 1, placed 1.

| plant | sign | F | key | fillers | echoes | plain rank / z | free-null rank / z | e56 rank / z / acc | decode (first 44) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | sub | 0 | phrase-3 MASTER STOPPED THE | 32 | 1 | 423 / 2.7 | 1 / 11.8 | 1 / 86.7 / 0.94 | THESLOUGHWHICHWASNEXTTOHISOWNHOUSESOAWAYHEWE |
| 8 | beaufort | 0 | vigenere-word-rev SACREDʳ | 33 | 3 | 194 / 2.6 | 1 / 10.7 | 1 / 93.6 / 0.95 | NOTTELLHOWTOPARTWITHMINEOLDCOMPANIANSTHEIRPR |
| 16 | add | 1 | self running key plaintext@773 | 25 | 3 | 6 / 6.1 | 3 / 14.0 | 1 / 68.8 / 0.87 | THNGSALSOBITEMEANDLICEABURNNGWORCCANSTTHOUNO |
| 24 | sub | 0 | self running key plaintext@679 | 25 | 1 | 2 / 5.2 | 3 / 13.9 | 1 / 82.8 / 0.88 | COULDNOTTELLWHATTODOUNTILIBRACEMYMINDTOFAITH |
| 1 | add | 0 | phrase-4 IS ONLY THROUGH GOING | 30 | 1 | 3870 / -0.1 | 1 / 13.2 | 1 / 52.3 / 0.64 | HEDESCRIBETHEBEASTTHATISCLEANHEISSUCHAONETHA |
| 9 | sub | 1 | self running key plaintext@707 | 21 | 1 | 3681 / 0.7 | 1 / 13.4 | 1 / 77.3 / 0.92 | THENSAIDIAMSUREOFTHEENOWANDWITHTHATHEHADALMO |
| 17 | beaufort | 1 | phrase-3-rev CERTAINTY AND YOUR ʳ | 30 | 3 | 700 / 1.8 | 1 / 12.8 | 1 / 86.3 / 0.96 | PRISONERSANDWITHALTHEOLDGIANTWONDEREDTHATHEC |
| 25 | add | 0 | phrase-3 MASTER REPLIED THEN | 22 | 3 | 3310 / 0.5 | 1 / 13.1 | 1 / 89.1 / 0.97 | STOPPEDANDBEGANTOMUSEWHATHEHADBESTTODOSOMETI |
| 2 | beaufort | 0 | self running key plaintext@2957 | 30 | 2 | 593 / 2.0 | 6 / 13.3 | 1 / 78.2 / 0.89 | DANGEROUSYETTHISSECONDPARTWHICHHEWASYETTOGOW |
| 10 | add | 1 | vigenere-word CIRCUMFERENCES | 29 | 1 | 6 / 5.1 | 1 / 12.9 | 1 / 83.5 / 0.91 | ANDCHILDRENANDBRETHRENANDSISTERSANDHISOWNLIF |
| 18 | sub | 0 | phrase-2 IS NOT | 22 | 3 | 7 / 4.1 | 1 / 12.3 | 1 / 98.2 / 0.89 | RELIGIANFORTHEWORLDWILLTHROWAWAYRELIGIANFORT |
| 26 | beaufort | 0 | vigenere-word-rev CONSUMEʳ | 30 | 4 | 462 / 2.3 | 1 / 13.2 | 1 / 93.5 / 1.00 | IHAUESAIDCONCERNNGOURSELUESWHENOURTHOUGHTSOF |
| 3 | sub | 1 | affine position 13·n+4 | 31 | 3 | 1 / 4.7 | 1 / 11.3 | 1 / 81.9 / 0.90 | INTOGODBOOCANDTHATMYNOWOFFFTHATSCORETHEREFOR |
| 11 | beaufort | 1 | self running key plaintext@1359 | 25 | 1 | 8 / 5.2 | 1 / 14.9 | 1 / 78.4 / 0.94 | ANDFROMTHEWAYTHERETOHATHTHISWICCEDMANTURNEDT |
| 19 | add | 0 | phrase-4 IS NOTHING TO BE | 31 | 0 | 438 / 2.4 | 1 / 11.9 | 1 / 85.7 / 1.00 | ROUGHINTHATPLACETHEYCHOSETOGOOUTOFITINTOTHAT |
| 27 | sub | 1 | self running key plaintext@1580 | 31 | 1 | 58 / 2.8 | 1 / 11.9 | 1 / 76.7 / 0.98 | THITHERIFELLINHEREHELPBUTWHYDIDNOTYOULOOCFOR |
| 4 | add | 1 | self running key plaintext@1788 | 33 | 0 | 652 / 1.9 | 1 / 10.6 | 1 / 81.5 / 0.97 | SOSOONASTHEMANOUERTOOCMEHEWASBUTAWORDANDABLO |
| 12 | sub | 0 | affine position 22·n+16 | 23 | 2 | 330 / 1.7 | 3 / 13.4 | 1 / 96.2 / 1.00 | BIDTHEMBEWAREOFTHEFLATTERERTHETHIRDBIDTHEMTA |
| 20 | beaufort | 0 | self running key plaintext@1517 | 28 | 1 | 5848 / -0.1 | 1 / 11.8 | 1 / 78.1 / 0.85 | BACCWITHACOUETOUSHEARTWHENSHEWASGONGFROMSODO |
| 28 | add | 1 | phrase-2 YOUR CERTAINTY | 28 | 0 | 47 / 3.4 | 1 / 11.6 | 1 / 70.0 / 0.91 | PASSIANWILLHAUEALLNOWTHISYEARTHATISTOSAYINTH |
| 5 | beaufort | 1 | phrase-3-rev OR THE MESSAGE ʳ | 32 | 1 | 183 / 3.5 | 1 / 11.4 | 1 / 80.6 / 0.94 | THELORDOFTHEHILLFORTHERELIEFANDSECURITYOFPIL |
| 13 | add | 0 | phrase-4-rev BE RIGHT ABOUT TO ʳ | 20 | 0 | 15 / 3.7 | 1 / 13.6 | 1 / 92.3 / 0.94 | LOWSNEACNGBUSINESSFORAMANTOMINDRELIGIANHESAI |
| 21 | sub | 1 | self running key plaintext@2225 | 26 | 2 | 280 / 3.4 | 3 / 14.8 | 1 / 90.7 / 0.98 | BEFOUNDTRUEMENATTHEENDOFTHEWAYYOUCOMEISISYOU |
| 29 | beaufort | 1 | affine position 7·n+19 | 32 | 1 | 572 / 0.9 | 3 / 12.2 | 1 / 82.5 / 0.96 | THEMWHENBYTHESEASSAULTEDANDYETNOTWITHSTANDNG |
| 6 | sub | 0 | primes p[n+4] | 30 | 2 | 5451 / -0.3 | 2 / 10.0 | 1 / 82.2 / 0.97 | SOSWEETLYHEINTHEHOLYSCRIPTUREFAITHTHATISTRUE |
| 14 | beaufort | 0 | affine position 5·n+0 | 27 | 0 | 1892 / 0.5 | 2 / 12.9 | 1 / 87.7 / 0.97 | RIGHTUPTHEHILLANDTHENAMEOFTHEGONGUPTHESIDEOF |
| 22 | add | 1 | primes+1 p[n+95]+1 | 29 | 2 | 2548 / 0.4 | 1 / 13.2 | 1 / 87.9 / 1.00 | AGAINANDWITHTHATHEBEATTHEMALLTHEWAYTHITHERTH |
| 7 | add | 0 | self running key plaintext@688 | 27 | 1 | 6 / 4.2 | 1 / 13.2 | 1 / 87.1 / 0.93 | THEIRLORDTHECNGAGAINSTHIMTHENSTOODFORTHENUYA |
| 15 | sub | 1 | self running key plaintext@231 | 24 | 2 | 3891 / 0.7 | 1 / 15.3 | 1 / 82.3 / 0.88 | GOODLYANDGARDENSARETHESEHEANSWEREDTHEYARETHE |
| 23 | beaufort | 1 | affine position 8·n+26 | 25 | 0 | 366 / 1.7 | 1 / 14.7 | 1 / 62.2 / 0.89 | BUTIFSHEBEFULLSHEOUTBOTHANDMACESTHEIRBLESSNG |

## Controls (six plants through the full library of their sign)

| cell | sign | F | key | rank | z | above null max | accuracy |
|---|---|---|---|---|---|---|---|
| 0 | sub | 0 | phrase-3 KNOW TO BE | 1 | 92.5 | yes | 0.96 |
| 1 | add | 0 | self running key plaintext@868 | 1 | 106.3 | yes | 0.92 |
| 2 | beaufort | 0 | phrase-4 FOUR UNREASONABLE THINGS EACH | 1 | 76.9 | yes | 0.84 |
| 3 | sub | 1 | phrase-2 ONLY WHAT | 1 | 75.0 | yes | 0.92 |
| 4 | add | 1 | phrase-4-rev AND THUS OUR DIVINITY ʳ | 1 | 88.8 | yes | 1.00 |
| 5 | beaufort | 1 | self running key plaintext@2670 | 1 | 67.4 | yes | 0.82 |

## The book's keys: 7,621 x 3 signs x 2 F x 55 pages

Pages 55; cells 330; keys at z ≥ 4.5: 507; largest z 7.32.

| page | sign | F | key | z | above null max | fillers | echoes | decode (first 60) |
|---|---|---|---|---|---|---|---|---|
| LP2-22 | beaufort | 0 | self running key plaintext@2824 | 7.32 | yes | 6 | 0 | ATHEAPOWYSTHOUTHEBREACTHE |
| LP2-02 | add | 1 | self running key plaintext@2679 | 7.24 | yes | 2 | 0 | ITHESOTHYONEOFFUELBYOF |
| LP2-34 | beaufort | 0 | phrase-2 THE MASTER | 6.99 | yes | 14 | 0 | ITOHEADONATNEARHEAUEMEANTWOAIDINLETWEEYEWITHSEENGMYTHE |
| LP2-49 | beaufort | 0 | self running key plaintext@314 | 6.94 | yes | 1 | 0 | THEITWERESEE |
| LP2-02 | add | 0 | self running key plaintext@2679 | 6.77 | yes | 2 | 0 | ITHESOTHYONEOFFUELBYOF |
| LP2-34 | beaufort | 1 | phrase-2 THE MASTER | 6.74 | yes | 14 | 0 | ITOHEADONATNEARHEAUEMEANTWOAIDINLETWEEYEWITHSEENGMYTHE |
| LP2-49 | beaufort | 1 | self running key plaintext@314 | 6.69 | yes | 1 | 0 | THEITWERESEE |
| LP2-40 | add | 0 | self running key plaintext@2272 | 6.51 | yes | 12 | 0 | ONIFOFSOYOUINGIUEIWASTOPANGSOSTAXEOFHOW |
| LP2-14 | add | 1 | primes-1 (totient) p[n+84]-1 | 6.50 | yes | 6 | 0 | MEPATTHROWFINDSOTOBEPUTTHE |
| LP2-14 | add | 0 | primes-1 (totient) p[n+84]-1 | 6.49 | yes | 6 | 0 | MEPATTHROWFINDSOTOBEPUTTHE |
| LP2-22 | beaufort | 1 | self running key plaintext@2824 | 6.43 | yes | 6 | 0 | ATHEAPOWYSTHOUTHEBREACTHE |
| LP2-51 | beaufort | 0 | self running key plaintext@416 | 6.37 | yes | 4 | 0 | TOSCIRTSHUMANONSO |
| LP2-51 | beaufort | 1 | phrase-2 DISCOVER AN | 6.32 | yes | 2 | 0 | TOSCIRTSDOESGOTOF |
| LP2-04 | add | 1 | phrase-3-rev TO STUDY HERE ʳ | 6.31 | yes | 10 | 0 | FEWAOFINHUNTHEOROFISTHNGDOTHENHERTHESHED |
| LP2-26 | add | 0 | self running key plaintext@289 | 6.27 | yes | 8 | 0 | ANDCNGDOONETISHEARISTHATOFTHEWAROHPUTAT |

## Prime streams: 3,000 x 3 signs x 2 F x 55 pages

Pages 55; cells 330; keys at z ≥ 4.5: 308; largest z 6.50.

| page | sign | F | key | z | above null max | fillers | echoes | decode (first 60) |
|---|---|---|---|---|---|---|---|---|
| LP2-14 | add | 1 | prime p-1 s=84 | 6.50 | yes | 6 | 0 | MEPATTHROWFINDSOTOBEPUTTHE |
| LP2-14 | add | 0 | prime p-1 s=84 | 6.49 | yes | 6 | 0 | MEPATTHROWFINDSOTOBEPUTTHE |
| LP2-27 | beaufort | 1 | prime p s=340 | 6.39 | yes | 7 | 0 | ANOHOFABLEGONGTOGODMANISLEFTAASCTODOORIS |
| LP2-44 | add | 0 | prime p s=321 | 6.10 | yes | 8 | 0 | ONTHEHADHASLYTASHEWOODEOLXTHECFLIANSALL |
| LP2-22 | add | 0 | prime p+1 s=829 | 5.81 | yes | 8 | 0 | ITAHEADATAOFHEARTISASTHY |
| LP2-21 | add | 0 | prime p-1 s=409 | 5.72 | yes | 8 | 0 | ISBEAMAIYETSUNGASOFTOOFITHATIA |
| LP2-22 | beaufort | 1 | prime p+1 s=360 | 5.71 | yes | 4 | 0 | ITTHEOFSHEWITHBYNEATIFFRO |
| LP2-32 | beaufort | 0 | prime p-1 s=233 | 5.71 | yes | 5 | 0 | IBEENRHUNPUTIOR |
| LP2-21 | add | 1 | prime p-1 s=409 | 5.71 | yes | 8 | 0 | ISBEAMAIYETSUNGASOFTOOFITHATIA |
| LP2-44 | add | 1 | prime p s=321 | 5.70 | yes | 8 | 0 | ONTHEHADHASLYTASHEWOODEOLXTHECFLIANSALL |
| LP2-15 | beaufort | 0 | prime p-1 s=532 | 5.68 | yes | 10 | 0 | IMONAGREETHEEMYIITOFOHSONGITEAUOURON |
| LP2-31 | sub | 1 | prime p+1 s=129 | 5.68 | yes | 8 | 0 | IFOFMRBRNGOLDINLIUNGISTOINDEARAOLDTHEERUETHEN |
| LP2-32 | add | 0 | prime p-1 s=361 | 5.62 | yes | 4 | 0 | AGATEWHOTENIMOUTH |
| LP2-53 | beaufort | 1 | prime p s=742 | 5.61 | yes | 5 | 0 | THEEOFMEANHAIRMEEASYNOITFROMHE |
| LP2-27 | beaufort | 0 | prime p-1 s=423 | 5.57 | yes | 7 | 0 | MYTHEEUETHNGTHEIFORISISTOITHATUS |

## Claims

- E1 this decoder recovers ≥ 27 of 30 plants: **holds**.
- E2 its recoveries ≥ the free-null decoder's: **holds**.
- E3 no candidate over the book's keys: **fails** (25 rows).
- E4 no candidate over the prime streams: **fails** (4 rows).

Reading: written after the run. [stated — the tables]
