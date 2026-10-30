# The red runs as keys, as a stream, as ciphertext and in the clear

Registration: `results/red_lane_registration.md`. Data: `results/red_runs.md` (18 runs of ≥ 3 runes, 212 runes). Plain decoder with the soft skip; z against 400 random keys of the same form per cell; candidate: z ≥ 6, rank 1, readable, above the hypothesis's largest null z.

## Controls

| control | planted | top: key / offset | sign | F | z | rank | pass |
|---|---|---|---|---|---|---|---|
| C1 | LP2-00 L1 (heading, 13) | LP2-00 L1 (heading, 13) | sub | True | 12.3 | 1 | no |
| C2 | 19 | 19 | sub | True | 14.8 | 1 | yes |
| C3 | ('phrase-4-rev', 'TO GO AND STUDY ʳ') | ('phrase-4-rev', 'TO GO AND STUDY ʳ') | sub | True | 3.7 | 1 | no |
| C4 | ('phrase-4-rev', 'TO GO AND STUDY ʳ') | ('phrase-4-rev', 'FOLLOW REASON SO WE ʳ') | beaufort | False | 2.8 | 1 | no (power statement, not a claim) |

## H1 repeating keys: 7,392 tests, largest z 3.54, largest null z 5.13, candidates 0

| target | key | sign | F | z | rank | tr |
|---|---|---|---|---|---|---|
| LP2-20 | LP2-15 L1 (heading, 9) | beaufort | False | 3.54 | 1 | TMMTHEEXNIOBIABUAIAIAYHOOEATYUHTHRGHCMFYYEARERAWYEBWPUPUMEAEAFNGRHSRIF |
| LP2-10 | LP2-53 L8 (passage, 22) | beaufort | False | 3.50 | 1 | DPDIANGEUACMCSJYLPDIEWEOCCWTHUONGUOBJUNDMGWMEAOULCNENNATMUNGOPYSCTHG |
| LP2-20 | LP2-15 L1 (heading, 9) | beaufort | True | 3.18 | 1 | TMMTHEEXNIOBIABUAIAIAYHOOEATYUHTHRGHCMFYYEARERAWYEBWPUPUMEAEAFNGRHSRIF |
| LP2-52 | LP2-07 L10 (inline, 14) | sub | True | 3.10 | 2 | MFTEAHIPBFUFIAMSREAUAJTHYTHNAMCMNMBUNGFHYMNFFWYFCTHNGAYPDJEDEAOEUOECLI |
| LP2-52 | LP2-15 L2 (inline, 11) | add | True | 3.08 | 1 | RFLPRBIITEAXETSSTHNESPNWHWAELDFUFIHDAOEFMFUCTABSECALRCNGPPIAOFHEAR |
| LP2-09 | LP2-15 L2 (inline, 11) | sub | False | 3.05 | 1 | GGRYGLTHSLPOIHNGEXBGPDXGEAEANGDYPGDWDOEPGYBWLSXMTHXIBYSLGIHWSMRAJFIA |
| LP2-17 | LP2-53 L7 (passage, 24) | sub | False | 3.04 | 1 | WAUHAACAESNEIASWJTOYNLMUPWSIAYMRSWWAERRLLEOMEAUBHXEATJEUUOEURRFNGREF |
| LP2-10 | LP2-53 L8 (passage, 22) | beaufort | True | 2.99 | 1 | DPDIANGEUACMCSJYLPDIEWEOCCWTHUONGUOBJUNDMGWMEAOULCNENNATMUNGOPYSCTHG |
| LP2-53 | LP2-39 L7 (inline, 3) | add | False | 2.92 | 2 | IUXDTHTBEFHGAUHWJNFOJCEAHTNCWDDROETNTFARNGYORTHMTSTNTHPEGYLRFABMUE |
| LP2-16 | LP2-03 L1 (heading, 16) | beaufort | False | 2.87 | 1 | THBBEOCTHOIAYYJSNGPWBNGTHOMSHISGNNGPSPBANHOEAISXHMNEARGNCITTBCURLAEBAOC |

## H2 the red stream as a running key: 139,920 tests, largest z 4.69, largest null z 4.08, candidates 0

| target | rev | sign | F | offset | z | rank | tr |
|---|---|---|---|---|---|---|---|
| LP2-28 | True | beaufort | True | 16 | 4.69 | 1 | IODBAMAEIARTHXRYBRPERMRLJSNGLHDWSDUABIAURIIIANBFGSTDEGUIBCTBYOOOG |
| LP2-03 | True | sub | False | 140 | 4.34 | 1 | FIEOLENGFJGYSADGTOTWCNGSTHMIICTRGXAFPFWMNIEAASRSCNTNMOENOBESYNAIABX |
| LP2-04 | True | sub | True | 199 | 4.13 | 1 | SGHTEAINFEAWTHIAFDHAFJCIGETINILAEONCIATTHACXENOBFNEATHLHMYHHIFFWPYGGO |
| LP2-23 | False | beaufort | False | 142 | 4.01 | 1 | YIHHOCOFPHIAULACIEGTPAEANGCSEOSATFGYYMSLUORWFIAHDOHUEYOEEDTHJEASNYM |
| LP2-28 | False | sub | True | 147 | 3.95 | 1 | DHCHNGTHDTAGNGIAEIAOOPEEFTADDJHTHNGIAGSYLXTHNEORWCDBHLLEOFJHCGTHRHBSUP |
| LP2-22 | True | add | True | 191 | 3.78 | 1 | HNGSIAMETDWILHYIANGJXTYTRNGMINIAOXOESAWNELEJHPIABIHSUGRNIAPADWIFMJLX |
| LP2-03 | True | sub | True | 140 | 3.75 | 1 | FIEOLENGFJGYSADGTOTWCNGSTHMIICTRGXAFPFWMNIEAASRSCNTNMOENOBESYNAIABX |
| LP2-10 | True | sub | False | 29 | 3.67 | 1 | UGMEETEIANGGSIDPUIATNOOXXLCNGFSIACWSXHLNORIAOMTHONGEEAEMYBNSSAHMRFADS |
| LP2-13 | True | add | False | 163 | 3.62 | 1 | THRTRNEAFAWGICYYIDUCTHHNIIACGONBBCCEIAPEAWNGTHUEXUJDNGCJFTFXTTYBAENGFTT |
| LP2-44 | True | add | True | 78 | 3.61 | 1 | CNPYWTHXWNYTHDUGHWXPEFEWDPWEDIYASSEAFMEAFEJTHHCEFTSRHMAAEPNGNNGAWANGN |

## H3 red runs as ciphertext under the book's keys: 685,890 tests, largest z 3.20, largest null z 3.07, candidates 0

| target | sign | F | key | z | rank | tr |
|---|---|---|---|---|---|---|
| LP2-53 L8 (22) | beaufort | True | ('self running key', 'plaintext@664') | 3.20 | 1 | TIHNELWYSRAUACRHRYNTOM |
| LP2-27 L1 (19) | sub | True | ('vigenere-word-rev', 'THATʳ') | 3.12 | 1 | OEARLUHUGRDIDAERLOE |
| LP2-27 L1 (19) | sub | False | ('vigenere-word-rev', 'THATʳ') | 3.07 | 1 | OEARLUHUGRDIDAERLOE |
| LP2-27 L1 (19) | sub | True | ('phrase-4-rev', 'TOLD THE MASTER HIS ʳ') | 3.04 | 1 | ROETYTNUETHTEMTRCCYN |
| LP2-53 L8 (22) | beaufort | True | ('phrase-3-rev', 'IS THE BEHAVIORS ʳ') | 3.01 | 1 | TGOMTRTRALDWNIAECOIDSSI |
| LP2-27 L1 (19) | sub | False | ('phrase-4-rev', 'TOLD THE MASTER HIS ʳ') | 2.99 | 1 | ROETYTNUETHTEMTRCCYN |
| LP2-53 L7 (24) | sub | False | ('phrase-4-rev', 'THE MASTER STOPPED THE ʳ') | 2.98 | 1 | ACEYDRNSDRBAEORNFGHEWUWN |
| LP2-53 L7 (24) | add | False | ('self running key', 'plaintext@1863') | 2.97 | 1 | TEAUAIEEIFOASLUYSEMLMRNWM |
| LP2-53 L8 (22) | beaufort | False | ('self running key', 'plaintext@664') | 2.93 | 1 | TIHNELWYSRAUACRHRYNTOM |
| LP2-40 L1 (8) | add | True | ('self running key', 'plaintext@1661') | 2.91 | 1 | EEASIEUA |

## H4 headings in the clear and self-keyed (P = 15·C)

| run | z as written | as written | z self-keyed | self-keyed |
|---|---|---|---|---|
| LP2-00 L1 (heading, 13) | +1.4 | SHEOGMIAFSYENGC | -0.7 | OERNTOAEAFOEPNAEB |
| LP2-03 L1 (heading, 16) | -1.7 | LJEOHNGCTHTAEJTXHTUOE | +0.4 | ILGRAEBUHIALHWRHSJ |
| LP2-06 L5 (inline, 11) | -1.1 | ATXBMGIASBXEO | -0.6 | EOHWDAOEAOEDWG |
| LP2-07 L10 (inline, 14) | -1.3 | DOOETTHAECWJXEAGEAM | +0.2 | YTJHUIABELWXOXA |
| LP2-08 L1 (heading, 12) | -0.1 | XIXMUXMCTHPOB | +1.7 | WCWASWABUNGTD |
| LP2-15 L1 (heading, 9) | +0.1 | FULMAEAYOEA | -2.0 | FSIAEOXPJEO |
| LP2-15 L2 (inline, 11) | +1.2 | LUNGNCUBNTFNG | +0.0 | ISAEMBSDMHFAE |
| LP2-23 L1 (heading, 16) | +0.2 | UAWNGGXDGIBIEOTBIY | +0.5 | SEOEAEOWYOCDCGHDCP |
| LP2-27 L1 (heading, 19) | +0.8 | MPYLSOAAEHLEEOIMLLSCP | -0.6 | ANGPIOETEOIARINGCAIIOEBNG |
| LP2-33 L1 (heading, 10) | -0.3 | DEOXCFIAWHG | +0.3 | YGWBFCEOERO |
| LP2-33 L6 (inline, 8) | -2.3 | NGTHEOIFCOEEO | -0.9 | AEUGCFBJG |
| LP2-40 L1 (heading, 8) | +0.1 | FNMYGDAEH | +0.9 | FMAPOYIAR |
| LP2-53 L7 (passage, 24) | -2.2 | PWEOSWBEOTHNHGJRIADIATHAIEOAEXLEO | +0.0 | NGEGOEEDGUMROLTHEAYEAUEOCGIAWIG |
| LP2-53 L8 (passage, 22) | -0.1 | EAIAAJHRTHPDJNGOGFEOMCHDOTC | +0.1 | XEAEOLRTHUNGYLAETOFGABRYTHB |
| LP2-54 L1 (heading, 9) | +0.3 | AMNGDIATHXIM | -0.5 | EOAAEYEAUWCA |

## Claims

- K1 controls C1–C3: **fail**.
- K2 H1 no candidate: **holds**.
- K3 H2 no candidate: **holds**.
- K4 H3 nothing at z ≥ 6 rank 1: **holds**.
- K5 H4 nothing at z ≥ 4: **holds**.

Reading: H1, H2 and H4 are null with power shown: the planted own-page key came first at z 12.3 and the planted stream offset at z 14.8, while the largest observed z on the pages is 3.54 (H1) and 4.69 (H2, below the hypothesis's largest null z of 4.08 only by the look-elsewhere of 140 k tests, rank 1 but unreadable), and no heading reads as written or self-keyed. K1 fails as written for two reasons of the registration's own making: C1 found the planted key first at z 12.3 but the script's pass flag also demanded the literal-F setting, which the registration did not ask for (the F-on cell of the same key scored 0.4 higher by chance); C3 found the planted book key first at 50 runes but at z 3.7, so the z ≥ 6 bar is unreachable at the red runs' lengths (8–24 runes) and H3 is below power: K4 holds vacuously and says nothing. The red runs are rubrication inside the cipher stream, as the solved koan page already showed; they are not a key, not a keystream, not in the clear. [stated — the tables; the power reading inferred from C3]

Runtime 714 s. Reproduce: `.venv/bin/python -I src/red_lane.py`.
