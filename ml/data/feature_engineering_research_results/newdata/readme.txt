kun other field on avattu, niin luokkaan other_field kuuluvat (vapaata tekstiä kirjoittaneet) on avattu niin, että vapaa kirjoitus luokitellaan omaksi studyfield luokaksi. 

(huom! kirjoitusvirheillä ja isoilla kirjaimilla on väliä, eikä tässä myöskään oteta huomioon muuta tapaa kirjoittaa sama asia.)
esim. Industrial Management on eri kuin Industrial Management and Engineering

kun other_field on suljettu, niin kaikki vapaa teksti on yksi luokka nimeltä other_field.

hakemusten samanlaisuudessa käytetty SBERTin mallia 'all-MiniLM-L6-v2'. Ja samanlaisuus laskettiin cosine läheisyydellä (distance.cosine).

hakemusten tunteita testattiin 'j-hartmann/emotion-english-distilroberta-base' mallilla "text-classification" avulla.