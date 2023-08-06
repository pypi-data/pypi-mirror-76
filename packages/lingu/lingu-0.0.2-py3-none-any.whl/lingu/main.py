from lingu.correctors.text import spell_check, spell_check_neat
from lingu.ocr.postprocessing import correct

from lingu.ocr.postprocessing import correct

def main():
    with open("../testfiles/3.txt") as f:
        ftext = f.read()  # .replace('\n', ' ')
    """
    DEBUG:
    Stutt setning: "Þinngið samþikkti tilöguna"

    """
    b1 = """Orðin sem lágu í loftinu

    fæddust ínn Í fylgsni hugans
    
    og héldu áfram að valda sársauka
    löngu eftir að þau voru sögð.
    
    Höggin sem dynja á nóttunni.
    Marið á kinninni.
    
    Örin á sálinni.
    
    Þungi þinn
    
    Þegar þú notar líkama minn.
    
    Ég ber þig á herðunum
    
    ég næ ekki andanum.
    
    Ég leggst á hnéin og bið almættið
    að lýsa upp svartnættið.
    
    Ég er kona, í karlaveldi.
    
    Í Kabul, í Afganistan.
    
    Ég hef alltaf búið við ofbeldi.
    En það snertir engan.
    
    Munið mig í landinu fjær
    móður sem á dætur tvær,
    verndið þær.
    
    Ég er raddlaus hulin mær
    Huldumær."""
    b2 = "3. janúir sl. keypti ég 64kWst rafbíl. Hann kostaði € 30.000. Það er mega fínt."
    b3 = "fæddust ínn Í fylgsni hugans"
    fintext = correct(b2+b1, **{"reynir": True, "ngrams": True, "ngrams_nr_of_succ": 20})
    print(fintext)


    #ftext = "sjavar" #"Þinngið samþikkti tilöguna.\n sldk\nkk\nkk.k Það var er betir ap vera svona. En svo var það ekki"#". Það var er betir ap vera svona. "
    #print(ftext)
    #correct(ftext)




    #spell_check_neat(ftext)
    # spell_check(ftext)


if __name__ == "__main__":
    main()