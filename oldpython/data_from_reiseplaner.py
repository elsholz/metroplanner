

data1 = """
Feldmark Marktplatz, Wesel 	an 11:12 	ab 11:12 		 

Tilsiter Str., Wesel 	an 11:13 	ab 11:13 		 
Rastenburger Straße, Wesel 	an 11:14 	ab 11:14 		 
Kartäuserweg, Wesel 	an 11:15 	ab 11:15 		 
Breiter Weg, Wesel 	an 11:16 	ab 11:16 		 
Blankenburgstraße, Wesel 	an 11:17 	ab 11:17 		 
Mölderplatz, Wesel 	an 11:19 	ab 11:19 		 
Mathenakreuz, Wesel 	an 11:21 	ab 11:21 		 

"""

def conv(data, y=80):
    for idx, ln in enumerate([l.strip() for l in data.splitlines() if l.strip()]):
        stop, *_ = ln.split("\t")
        # print(stop)
        print(f""""{stop[:5].lower()}": {"{"}
            name: "{stop.split(',')[0]}",
            location: [
                {idx * 2 + 1}, {y}
            ],
        {"}"},""")

data2 = """
Bislich Ortsmitte, Wesel 	  	ab 11:21 		
Harsumer Weg, Wesel 	an 11:22 	ab 11:22 		 
Mühlenfeld, Wesel 	an 11:24 	ab 11:24 		 
Schüttwich, Wesel 	an 11:25 	ab 11:25 		 
Westerheide, Wesel 	an 11:26 	ab 11:26 		 
Mars, Wesel 	an 11:27 	ab 11:27 		 
Diersfordt Rosenallee, Wesel 	an 11:28 	ab 11:28 		 
Flüren Friedhof, Wesel 	an 11:29 	ab 11:29 		 
Flüren Waldstraße, Wesel 	an 11:31 	ab 11:31 		 
Flüren Altrheinstraße, Wesel 	an 11:32 	ab 11:32 		 
Flüren Drosselstraße, Wesel 	an 11:33 	ab 11:33 		 
Flüren Waldschenke, Wesel 	an 11:34 	ab 11:34 		 
Flüren Markt, Wesel 	an 11:35 	ab 11:35 		 
Flüren Beethovenstraße, Wesel 	an 11:36 	ab 11:36 		 
Flürener Weg, Wesel 	an 11:37 	ab 11:37 		 
Glückauf, Wesel 	an 11:38 	ab 11:38 		 
Eissporthalle, Wesel 	an 11:41 	ab 11:41 		 
Barthel-Bruyn-Weg, Wesel 	an 11:42 	ab 11:42 		 
Ackerstraße, Wesel 	an 11:43 	ab 11:43 		 
Friedrich-Geselschap-Str., Wesel 	an 11:44 	ab 11:44 		 
Feldmark Marktplatz, Wesel 	an 11:45 	ab 11:45 		 
Arbeitsagentur, Wesel 	an 11:47 	ab 11:47 		 
Kreishaus, Wesel 	an 11:48 	ab 11:48 		 
Amtsgericht, Wesel 	an 11:49 	ab 11:49 		 
Großer Markt, Wesel 	an 11:51 	ab 11:51 		 
Stettiner Straße, Wesel 	an 11:52 	ab 11:52 		 
Wallstraße, Wesel 	an 11:53 	ab 11:53 		 
Bahnhof, Wesel 	an 11:57 	ab 11:59 		 
Isselstraße, Wesel 	an 12:02 	ab 12:02 		 
Brüner Landstraße, Wesel 	an 12:04 	ab 12:04 		 
Franziskusstraße, Wesel 	an 12:05 	ab 12:05 		 
Schepersweg, Wesel 	an 12:06 	ab 12:06 		 
Am Schwan, Wesel 	an 12:07 	ab 12:07 		 
Kastanienstraße, Wesel 	an 12:08 	ab 12:08 		 
Am Lauerhaas, Wesel 	an 12:09 	ab 12:09 		 
Tannenstraße, Wesel 	an 12:10 	ab 12:10 		 
Eichenstraße, Wesel 	an 12:11 	ab 12:11 		 
Am Friedenshof, Wesel 	an 12:12 	ab 12:12 		 
Voßhöveler Straße, Wesel 	an 12:13 	ab 12:13 		 
Rudolf-Diesel-Straße, Wesel 	an 12:14 	ab 12:14 		 
Im Buttendicksfeld, Wesel"""
re19 = """Arnhem Centraal 	  	ab 15:45 	6b 	
Zevenaar 	an 15:54 	ab 15:54 	3 	 
Emmerich-Elten 	an 16:00 	ab 16:00 	2 	 
Emmerich 	an 16:06 	ab 16:09 	2 	 
Praest 	an 16:13 	ab 16:13 	1 	 
Millingen(b Rees) 	an 16:16 	ab 16:17 	1 	 
Empel-Rees 	an 16:19 	ab 16:20 	1 	 
Haldern(Rheinl) 	an 16:23 	ab 16:23 	1 	 
Mehrhoog 	an 16:27 	ab 16:28 	1 	 
Wesel Feldmark 	an 16:34 	ab 16:34 	1 	 
Wesel 	an 16:40 	ab 16:43 	3 	 
Friedrichsfeld(Niederrhein) 	an 16:46 	ab 16:46 	2 	 
Voerde(Niederrhein) 	an 16:49 	ab 16:50 	1 	 
Dinslaken 	an 16:53 	ab 16:54 	1 	 
Oberhausen-Holten 	an 16:58 	ab 16:58 	1 	 
Oberhausen-Sterkrade 	an 17:01 	ab 17:02 	2 	 
Oberhausen Hbf 	an 17:07 	ab 17:08 	12 	 
Duisburg Hbf 	an 17:15 	ab 17:16 	2 	 
Düsseldorf Flughafen 	an 17:24 	ab 17:25 	6 	 
Düsseldorf Hbf 	an 17:33 	  	4 	  """
re19a = """
Wesel-Blumenkamp 	an 18:22 	ab 18:23 	1 	 
Hamminkeln 	an 18:27 	ab 18:30 	1 	 
Hamminkeln-Dingden 	an 18:34 	ab 18:35 	1 	 
Bocholt 	an 18:42 	  	3 """

sb6 = """
Bahnhof, Xanten 	  	ab 17:58 		
Bahnhofstraße, Xanten 	an 17:59 	ab 17:59 		 
Gymnasium, Xanten 	an 18:00 	ab 18:00 		 
Friedhof, Xanten 	an 18:01 	ab 18:01 		 
Viktorstraße, Xanten 	an 18:02 	ab 18:02 		 
Haus Lau, Xanten 	an 18:06 	ab 18:06 		 
Birten Gewerbegebiet Birten, Xanten 	an 18:07 	ab 18:07 		 
Birten Gindericher Straße, Xanten 	an 18:08 	ab 18:08 		 
Ginderich Poll, Wesel 	an 18:12 	ab 18:12 		 
Ginderich Post, Wesel 	an 18:14 	ab 18:14 		 
Restaurant Lindenwirtin, Wesel 	an 18:20 	ab 18:20 		 
LVR-Niederrheinmuseum, Wesel 	an 18:21 	ab 18:21 		 
Norbertstraße, Wesel 	an 18:22 	ab 18:22 		 
Großer Markt, Wesel 	an 18:23 	ab 18:23 		 
Stettiner Straße, Wesel 	an 18:25 	ab 18:25 		 
Wallstraße, Wesel 	an 18:26 	ab 18:26 		 
Bahnhof, Wesel 	an 18:27 	  		  """
sb21 = """Bahnhof, Wesel 	  	ab 18:00 		
Post, Wesel 	an 18:02 	ab 18:02 		 
Drevenacker Straße, Wesel 	an 18:04 	ab 18:04 		 
Raesfelder Straße, Wesel 	an 18:05 	ab 18:05 		 
Ev. Krankenhaus, Wesel 	an 18:06 	ab 18:06 		 
Am langen Reck, Wesel 	an 18:07 	ab 18:07 		 
Am Dülmen, Wesel 	an 18:09 	ab 18:09 		 
Loher Weg, Wesel 	an 18:10 	ab 18:10 		 
Drevenack Gühnen, Hünxe 	an 18:11 	ab 18:11 		 
Drevenack Strütchensweg, Hünxe 	an 18:12 	ab 18:12 		 
Drevenack Schürmann, Hünxe 	an 18:14 	ab 18:14 		 
Drevenack Wachtenbrink, Hünxe 	an 18:16 	ab 18:16 		 
Damm Wortelkamp, Schermbeck 	an 18:18 	ab 18:18 		 
Damm Molkerei, Schermbeck 	an 18:19 	ab 18:19 		 
Bricht, Schermbeck 	an 18:21 	ab 18:21 		 
Hecheltjen, Schermbeck 	an 18:23 	ab 18:23 		 
Rathaus, Schermbeck 	an 18:24 	  		  """
bus68 = """Bahnhof, Wesel 	  	ab 18:28 		
Wallstraße, Wesel 	an 18:30 	ab 18:30 		 
Stettiner Straße, Wesel 	an 18:32 	ab 18:32 		 
Großer Markt, Wesel 	an 18:33 	ab 18:33 		 
Norbertstraße, Wesel 	an 18:34 	ab 18:34 		 
LVR-Niederrheinmuseum, Wesel 	an 18:35 	ab 18:35 		 
Restaurant Lindenwirtin, Wesel 	an 18:36 	ab 18:36 		 
Büderich Friedhof, Wesel 	an 18:40 	ab 18:40 		 
Büderich Marktstraße, Wesel 	an 18:40 	ab 18:40 		 
Winkeling, Wesel 	an 18:41 	ab 18:41 		 
Elvericher Weg, Wesel 	an 18:42 	ab 18:42 		 
Hotel Bürick, Wesel 	an 18:43 	ab 18:43 		 
Wallacher Weg, Rheinberg 	an 18:43 	ab 18:43 		 
Borth Solvay, Rheinberg 	an 18:44 	ab 18:44 		 
Borth Kolkstraße, Rheinberg 	an 18:45 	ab 18:45 		 
Borth Kirche, Rheinberg 	an 18:46 	ab 18:46 		 
Borth Ulmenallee, Rheinberg 	an 18:46 	ab 18:46 		 
Borth Bortherfeld, Rheinberg 	an 18:47 	ab 18:47 		 
Ossenberg Maas, Rheinberg 	an 18:49 	ab 18:49 		 
Ossenberg Kirche, Rheinberg 	an 18:50 	ab 18:50 		 
Solvay, Rheinberg 	an 18:52 	ab 18:52 		 
Ziegeleistraße, Rheinberg 	an 18:53 	ab 18:53 		 
Sportplatz, Rheinberg 	an 18:54 	ab 18:54 		 
Dr.-Aloys-Wittrup-Straße, Rheinberg 	an 18:55 	ab 18:55 		 
Innenwall, Rheinberg 	an 18:56 	ab 18:56 		 
Rathaus, Rheinberg 	an 18:58 	ab 18:58 		 
Krankenhaus, Rheinberg 	an 19:00 	ab 19:00 		 
Gewerbegebiet, Rheinberg 	an 19:02 	ab 19:02 		 
Winterswick, Rheinberg 	an 19:05 	ab 19:05 		 
Rheinkamp Reitweg, Moers 	an 19:09 	ab 19:09 		 
Riesengebirgsstraße, Moers 	an 19:11 	ab 19:11 		 
Utfort Rathaus, Moers 	an 19:13 	ab 19:13 		 
Kampstraße, Moers 	an 19:14 	ab 19:14 		 
Eurotec, Moers 	an 19:15 	ab 19:15 		 
Bethanien, Moers 	an 19:17 	ab 19:17 		 
Baerler Straße, Moers 	an 19:18 	ab 19:18 		 
Nordring, Moers 	an 19:19 	ab 19:19 		 
Königlicher Hof, Moers 	an 19:21 	ab 19:21 		 
Augustastr., Moers 	an 19:23 	ab 19:23 		 
Bahnhof, Moers 	an 19:27 	  		  """
sb3= """Schulzentrum-Mitte, Wesel 	  	ab 13:22 		
Bahnhof, Wesel 	an 13:26 	ab 13:26 		 
Post, Wesel 	an 13:28 	ab 13:28 		 
Drevenacker Straße, Wesel 	an 13:30 	ab 13:30 		 
Raesfelder Straße, Wesel 	an 13:31 	ab 13:31 		 
Ev. Krankenhaus, Wesel 	an 13:32 	ab 13:32 		 
Am langen Reck, Wesel 	an 13:33 	ab 13:33 		 
Am Dülmen, Wesel 	an 13:35 	ab 13:35 		 
Loher Weg, Wesel 	an 13:36 	ab 13:36 		 
Drevenack Gühnen, Hünxe 	an 13:37 	ab 13:37 		 
Bensumskamp, Hünxe 	an 13:49 	ab 13:49 		 
Busbahnhof, Hünxe 	an 13:50 	ab 13:50 		 
Markt, Hünxe 	an 13:51 	ab 13:51 		 
Stallbergsweg, Hünxe 	an 13:52 	ab 13:52 		 
Wilhelmstraße, Hünxe 	an 13:53 	ab 13:53 		 
Bruckhausen Witte Hus, Hünxe 	an 13:56 	ab 13:56 		 
Bruckhausen Lindenkamp, Hünxe 	an 13:57 	ab 13:57 		 
Bruckhausen Baßfeld, Hünxe 	an 13:59 	ab 13:59 		 
Bruckhausen Meesenweg, Hünxe 	an 14:01 	ab 14:01 		 
Knappenheim, Dinslaken 	an 14:02 	ab 14:02 		 
Bergpark Lohberg, Dinslaken 	an 14:03 	ab 14:03 		 
Schacht Lohberg, Dinslaken 	an 14:04 	ab 14:04 		 
Oeckinghaus, Dinslaken 	an 14:05 	ab 14:05 		 
Augustastraße, Dinslaken 	an 14:07 	ab 14:07 		 
Blumenanger, Dinslaken 	an 14:08 	ab 14:08 		 
Inkamp, Dinslaken 	an 14:09 	ab 14:09 		 
Gewerbegebiet Mitte, Dinslaken 	an 14:10 	ab 14:10 		 
Stadtwerke, Dinslaken 	an 14:11 	ab 14:11 		 
Neutor, Dinslaken 	an 14:12 	ab 14:12 		 
Bahnhof, Dinslaken 	an 14:14 """
bus68 = """
Bahnhof, Wesel 	  	ab 18:28 		
Wallstraße, Wesel 	an 18:30 	ab 18:30 		 
Stettiner Straße, Wesel 	an 18:32 	ab 18:32 		 
Großer Markt, Wesel 	an 18:33 	ab 18:33 		 
Norbertstraße, Wesel 	an 18:34 	ab 18:34 		 
LVR-Niederrheinmuseum, Wesel 	an 18:35 	ab 18:35 		 
Restaurant Lindenwirtin, Wesel 	an 18:36 	ab 18:36 		 
Büderich Friedhof, Wesel 	an 18:40 	ab 18:40 		 
Büderich Marktstraße, Wesel 	an 18:40 	ab 18:40 		 
Winkeling, Wesel 	an 18:41 	ab 18:41 		 
Elvericher Weg, Wesel 	an 18:42 	ab 18:42 		 
Hotel Bürick, Wesel 	an 18:43 	ab 18:43 		 
Wallacher Weg, Rheinberg 	an 18:43 	ab 18:43 		 
Borth Solvay, Rheinberg 	an 18:44 	ab 18:44 		 
Borth Kolkstraße, Rheinberg 	an 18:45 	ab 18:45 		 
Borth Kirche, Rheinberg 	an 18:46 	ab 18:46 		 
Borth Ulmenallee, Rheinberg 	an 18:46 	ab 18:46 		 
Borth Bortherfeld, Rheinberg 	an 18:47 	ab 18:47 		 
Ossenberg Maas, Rheinberg 	an 18:49 	ab 18:49 		 
Ossenberg Kirche, Rheinberg 	an 18:50 	ab 18:50 		 
Solvay, Rheinberg 	an 18:52 	ab 18:52 		 
Ziegeleistraße, Rheinberg 	an 18:53 	ab 18:53 		 
Sportplatz, Rheinberg 	an 18:54 	ab 18:54 		 
Dr.-Aloys-Wittrup-Straße, Rheinberg 	an 18:55 	ab 18:55 		 
Innenwall, Rheinberg 	an 18:56 	ab 18:56 		 
Rathaus, Rheinberg 	an 18:58 	ab 18:58 		 
Krankenhaus, Rheinberg 	an 19:00 	ab 19:00 		 
Gewerbegebiet, Rheinberg 	an 19:02 	ab 19:02 		 
Winterswick, Rheinberg 	an 19:05 	ab 19:05 		 
Rheinkamp Reitweg, Moers 	an 19:09 	ab 19:09 		 
Riesengebirgsstraße, Moers 	an 19:11 	ab 19:11 		 
Utfort Rathaus, Moers 	an 19:13 	ab 19:13 		 
Kampstraße, Moers 	an 19:14 	ab 19:14 		 
Eurotec, Moers 	an 19:15 	ab 19:15 		 
Bethanien, Moers 	an 19:17 	ab 19:17 		 
Baerler Straße, Moers 	an 19:18 	ab 19:18 		 
Nordring, Moers 	an 19:19 	ab 19:19 		 
Königlicher Hof, Moers 	an 19:21 	ab 19:21 		 
Augustastr., Moers 	an 19:23 	ab 19:23 		 
Bahnhof, Moers 	an 19:27 	  """

conv(bus68)




