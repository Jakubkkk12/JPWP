# JPWP
Configure basic network routing protocols (RIP, OSPF, BGP) with GUI

# Zadania 
Zadanie 1 (frontend - AL)
Zrefaktoruj kod tak aby zrobić jedno uniwersalne okienko RedistributionGUI (zamiast BGPRedistributionGUI, OSPFRedistributionGUI i RIPRedistributionGUI) i móc je zaaplikować do wszystkich protokołów routingu.

Zadanie 2 (backend - JK)
Stosując przyjętą w projekcie konwencję napisz odpowiednie funkcje umożliwiające obsłużenie dodania AREA w OSPF. Popatrz na ospf_area_add_gui.py aby zobaczyć jakie dane są zwracane z okienka. Prawidłowo rozwiązane zadanie powinno składać się z dopisanych funkcji w: frontend_backend_functions.py, universal_router_commands.py, commands.py oraz getting_ospf.py.

Zadanie 3 (frontend+backend - AL+JK)
Stosując Tkinter oraz przyjętą w projekcie konwencją na backend zaimplementuj możliwość stworzenia loopback interface (na urządzeniach cisco)  
