from idlelib.configdialog import changes

#Kezdeti tények
facts={
    "Laz":True,
    "Kohoges":True,
    "Torokfajas":True,
    "Izomfajas":True,
    "GyorsTesztPoz":True,
    "Szagvesztes":False,
    "KontakFerto":True,
    "KronikusBeteg":False,
    "Idos65Plusz":False
}
#Szabályok (feltételek -> következtetés)

rules=[
    (["Kohoges","Torokfajas"],"Megfazasgyanus"),
    (["Torokfajas","Laz","GyorsTesztPoz"],"StreptococcusGyanus"),
    (["Kohoges","Szagvesztes"],"CovidGyanus"),
    (["KontaktFerto","Kohoges"],"CovidGyanus"),
    (["MegfazasGyanus"],"OTC_Tunetkezeles"),
    (["StreptococcusGyanus"],"LaborPCR_Vagy_Torokkenet"),
    (["CovidGyanus"],"AntigenVagyPCR"),

    #Bayes -> teendők
    (["InfluenzaValoszinu"],"MaradjonOtthon"),
    (["InfluenzaValoszinu"],"FolyadekPihenes"),


    #admin lépések
    (["MaradjonOtthon"],"IgazolasSzukseges"),
    (["AntigenVagyPCR"],"TeszthelyKereses")
]

pA=0.10 #P(Influenza) -> prior
pF_A=0.80 #ha tényleg influenza van, 80% eséllyel lázas az illető
pF_not=0.15 # ha nincs influenza, 15% az esély hogy mégis lázas
pC_A,pC_not=0.70,0.20 #köhögés
pT_A,pT_not=0.85,0.05 #gyors teszt a pozitivitásra

def bayes_naive(pA,pF_A,pF_not,pC_A,pC_not,pT_A,pT_not,fever,cough,testpos):
    #Kimenet :P(Influenza| megfigyelések) -> posterior
    #P(H|E) = (P(E|H)*P(H))/P(E)
    #H=Influenza van
    #E= láz,köhögés és pozitív teszt
    #P(H)=prior esély
    #P(E)=likelihood
    #likelihood az influenza mellett
    like_A=1.0
    like_A*=(pF_A if fever else(1-pF_A))
    like_A*=(pC_A if cough else(1-pC_A))
    like_A*=(pT_A if testpos else(1-pT_A))


    #likelihood influenza nélkül
    like_not_A=1.0
    like_not_A *= (pF_not if fever else (1 - pF_not))
    like_not_A *= (pC_not if cough else (1 - pC_not))
    like_not_A *= (pT_not if testpos else (1 - pT_not))

    num=pA*like_A
    den=num + (1-pA) * like_not_A
    posterior=num/den
    return posterior

posterior=bayes_naive(pA,pF_A,pF_not,pC_A,pC_not,pT_A,pT_not,True,True,True)
print(f"P(Influenza|Tünetek) = {posterior:0.3f}")

treshold=0.5
if posterior>=treshold:
    facts["InfluenzaValoszinu"]=True

known=set()
for k in facts:
    if facts[k] is True:
        known.add(k)
print(known)

#addig futtatunk szabályokat, amíg új tény születik, ha már nem születik új, akkor megállunk
step=0# hány szabály "Tüzelt"
changed=True # változó, amely megmutatja hogy változott-e valami, az előző körben
while changed:
    changed=False
    i=0
    while i< len(rules):
    #rules:szabályok(feltételek,következtetés)
    #conds=Lista a feltételeéről concl = a következtetés
        conds,concl=rules[i]
        if concl in known:
            i+=1
            continue
        all_true=True
        j=0
        while j < len(conds):
            if conds[j] not in known:
                all_true=False
                break
            j+=1
        if all_true:
            known.add(concl)
            step+=1
            print(f"{step}. FIRE: [{', '.join(conds)}] => {concl}")
            changed=True
        i+=1
print("\nVégső igaz állítások (KNOWN) rendezve: ")
for t in sorted(known):
    print(" -",t)