#constants.py : 
from lib2to3.pygram import pattern_symbols


regular_letters = "abcdefghijklmnopqrstuvwxyz"
french_letters = "éàèùâêîôûçëïüœ"
considered_letters = regular_letters + french_letters

general_sing_titles = {"Monsieur", "Madame", "Mademoiselle"}
general_abbr_titles = {"M.", "Mme", "Mlle"}
general_plu_titles = {"Messieurs", "Mesdames", "Mesdemoiselles"}
general_titles = general_sing_titles.union(general_abbr_titles)

pro_sing_titles = {"Docteur", "Maître", "Professeur"}
pro_abbr_titles = {"Dr", "Me", "Pr"}
pro_titles = pro_sing_titles.union(pro_abbr_titles)

religious_sing_titles = {"Frère", "Mère", "Père", "Révérend Père", "Saint", "Sainte", "Sœur"}
religious_abbr_titles = {"F.", "M.", "P.", "R.P.", "St", "Ste", "Sr"}
religious_titles = religious_sing_titles.union(religious_abbr_titles)

obsolete_sing_titles = {"Monseigneur", "Veuve", "Votre Majesté", "Sa Majesté"}
obsolete_abbr_titles = {"Mgr.", "Vve", "V.M.", "S.M."}
obsolete_titles = obsolete_sing_titles.union(obsolete_abbr_titles)


especials = {
	"il y a":("il", "y ", "a",) , "Il y a":("Il_y_a",) ,
}

# patterns = {  
# 			# "test-il" : ("test","-il"),
# 			# "tost-il" : ("tost", "-il"),
# 			'il y a' : ('il', "y", "a"), 'Il y a' : ("Il", "y", "a") ,
# 			"qu'est-ce" : ("qu_est_ce",) , "Qu'est-ce" : ("Qu_est_ce", ) ,
# 			"quelques-uns" : ("quelques_uns",) ,  "Quelques-uns" : ("Quelques_uns",) , 
# 			"quelques-unes" : ("quelques_unes",) , "Quelques-unes" : ("Quelques_unes",) ,
# 			"faudra-t-il" : ("faudra", "-t_il" ), "Faudra-t-il" : ("Faudra", "-t_il") ,
# 			"fait-il" : ("fait", "-il") , "Fait-il" : ( "Fait", "-il" ),
# 			"doit-il" : ("doit", "-il") , "Doit-il" : ("Doit", "-il") ,
# 			"s'agit-il" : ("s'", "agit",  "il") , "S'agit-il" : ("S'", "agit", "-il" ),
# } 
# 			# 'il y a':'il_y_a', 'Il y a':'Il_y_a' 
# 			# [faudra][-t-il]","[fait][-il]","[doit][-il]”, “[s’][agit][-il]

patterns = {  
    # "test-il" : ("test","-il"),
    # "tost-il" : ("tost", "-il"),
    "qu'est-ce" : ("qu'est-ce",) , "Qu'est-ce" : ("Qu'est-ce", ) ,
    "quelques-uns" : ("quelques-uns",) ,  "Quelques-uns" : ("Quelques-uns",) , 
    "quelques-unes" : ("quelques-unes",) , "Quelques-unes" : ("Quelques-unes",) ,
    "faudra-t-il" : ("faudra", "-t-il" ), "Faudra-t-il" : ("Faudra", "-t-il") ,
    "fait-il" : ("fait", "-il") , "Fait-il" : ( "Fait", "-il" ),
    "doit-il" : ("doit", "-il") , "Doit-il" : ("Doit", "-il") ,
    "s'agit-il" : ("s'", "agit",  "il") , "S'agit-il" : ("S'", "agit", "-il" ),

    "c'est-à-dire" : ("c'est-à-dire",), "C'est-à-dire" : ("C'est-à-dire",),
    "d'accord" : ("d'accord",), "D'accord" : ("D'accord",),
    "entr'ouvèrt" : ("entr'ouvèrt",), "Entr'ouvèrt": ("Entr'ouvèrt",),
    "presqu'île" : ("presqu'île",), "Presqu'île": ("Presqu'île"),
    "peut- être": ("peut- être",), "Peut- être" : ("Peut- être"),
    "peut-être": ("peut-être",), "Peut-être" : ("Peut-être"),
    "au lieu de": ("au lieu de",), "Au lieu de": ("Au lieu de",),
    "du tout": ("du tout",), "Du tout": ("Du tout",),
    "au contraire": ("au contraire",), "Au contraire": ("Au contraire",),
    "bien que": ("bien que",), "Bien que": ("Bien que",), 
    "pomme de terre": ("pomme de terre",), "Pomme de terre": ("Pomme de terre",), "pommes de terre": ("pommes de terre",), "Pommes de terre": ("Pommes de terre",),
    "au revoir": ("au revoir",), "Au revoir": ("Au revoir",),
    "de rien": ("de rien",), "De rien": ("De rien",),
    "en train de": ("en train de",), "En train de": ("En train de",),
    "tout à fait": ("tout à fait",), "Tout à fait": ("Tout à fait",),
    "en effet": ("en effet",), "En effet":("En effet",),
    "au contraire": ("au contraire",), "Au contraire": ("Au contraire",),
    "à la fois": ("à la fois",), "A la fois": ("A la fois",),
    "avoir l'air": ("avoir l'air",), "Avoir l'air":("Avoir l'air",),
    "du coup": ("du coup",), "Du coup": ("Du coup",),
    "à la limite": ("à la limite"), "A la limite": ("A la limite",),
    "à la rigueur": ("à la rigueur"), "A la rigeur": ("A la rigeur",),
    "à peine": ("à peine",), "A peine": ("Apeine",),
    "au fait": ("au fait"), "Au fait": ("Au fait",),
    "vis-à-vis": ("vis-à-vis",), "Vis-à-vis": ("Vis-à-vis",),
    "au contraire": ("au contraire",), "Au contraire": ("Au contraire",),
    "d'ailleurs": ("d'ailleurs",), "D'ailleurs":("D'ailleurs",),
    "a priori": ("a priori",), "A priori": ("A priori",),
    "en fait": ("en fait",), "En fait": ("En fait",),
    "par contre": ("par contre",), "Par contre": ("Par contre",),
    "par example": ("par example",), "Par example": ("Par example",),
    "en retard": ("en retard",), "En retard": ("En retard",),
    "tout à l'heure": ("tout à l'heure",), "Tout à l'heure": ("Tout à l'heure",),
    "tout à coup": ("tout à coup",), "Tout à coup": ("Tout à coup",),
    "tout de suite": ("tout de suite",), "Tout de suite": ("Tout de suite",),

} 
# 'il y a' : ('il', "y", "a"), 'Il y a' : ("Il", "y", "a") ,