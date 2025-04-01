import time

# Définition du module de gestion des périphériques d'entrée/sortie
md_io = {
    "name": "gestion_peripherique",
    "composants": [
        {
            "device_controller": {
                "specs": {
                    "fabricant": "LogiTech",
                    "version_firmware": "v2.3",
                    "capacite_traitement": "100 opérations/s",
                    "interfaces": ["USB", "Bluetooth"],
                    "mode_operation": "Asynchrone",
                    "support_hotplug": True,
                    "protocoles": ["HID", "SCSI"],
                },
                "execution": {
                    "_DID": "D1001",         # Identifiant de l'opération en cours
                    "temps_ecoule_s": 0.0,     # Temps écoulé pour l'opération actuelle
                }
            },
            "liste_operations": [
                {
                    "DID": "D1001",
                    "Nom": "Lecture Clavier",
                    "Type": "Entrée",
                    "Priorite": "Normal",
                    "temps_prevu_s": 5.0
                },
                {
                    "DID": "D1002",
                    "Nom": "Mouvement Souris",
                    "Type": "Entrée",
                    "Priorite": "Normal",
                    "temps_prevu_s": 3.0
                },
                {
                    "DID": "D1003",
                    "Nom": "Impression Document",
                    "Type": "Sortie",
                    "Priorite": "Haut",
                    "temps_prevu_s": 10.0
                },
                {
                    "DID": "D1004",
                    "Nom": "Scan Image",
                    "Type": "Entrée",
                    "Priorite": "Normal",
                    "temps_prevu_s": 8.0
                },
            ],
            "file_IO": [
                {
                    "_DID": "D1001",
                    "status": "ready",
                    "temps_ecoule_deja": 0.0,
                }
            ]
        }
    ]
}

# Listes représentant les états des opérations I/O
operations_en_mode_waiting = ["D1002"]        # opérations en attente (ex. périphérique occupé)
operations_en_mode_ready = ["D1003", "D1004"]   # opérations prêtes à être traitées
operations_en_mode_processing = []              # opération(s) en cours de traitement
operations_en_mode_completed = ["D1005", "D1006"] # opérations déjà terminées (historique)

def execution_io():
    """
    Simule l'exécution d'une opération I/O.
    La fonction vérifie l'opération en cours, incrémente le temps écoulé et détermine
    si l'opération est terminée en comparant le temps écoulé avec le temps prévu.
    """
    temps_ecoule_s_operation = md_io["composants"][0]["device_controller"]["execution"]["temps_ecoule_s"]
    liste_operations = md_io["composants"][0]["liste_operations"]
    operation_encours = md_io["composants"][0]["device_controller"]["execution"]

    # Si l'opération en cours n'est ni en attente ni déjà terminée
    if (operation_encours["_DID"] not in operations_en_mode_waiting and
        operation_encours["_DID"] not in operations_en_mode_completed):

        # Recherche de l'opération correspondante dans la liste
        for op in liste_operations:
            if op["DID"] == operation_encours["_DID"]:
                temps_prevu_s_operation = op["temps_prevu_s"]
                operation_nom = op["Nom"]
                break
        else:
            print("Opération non trouvée dans la liste.")
            return False

        # Comparaison du temps écoulé avec le temps prévu
        if temps_ecoule_s_operation >= temps_prevu_s_operation:
            print(f"L'opération '{operation_nom}' ({operation_encours['_DID']}) est terminée")
            operations_en_mode_completed.append(operation_encours["_DID"])
            print("Opérations terminées:", operations_en_mode_completed)
            print("----------------------------------")
            return False
        else:
            print(f"L'opération '{operation_nom}' n'est pas terminée")
            print("Temps écoulé : ", temps_ecoule_s_operation)
            print("Temps prévu : ", temps_prevu_s_operation)
            print("Opérations terminées:", operations_en_mode_completed)
            print("----------------------------------")
            time.sleep(1)  # Simule le passage du temps
            temps_ecoule_s_operation += 1.0
            md_io["composants"][0]["device_controller"]["execution"]["temps_ecoule_s"] = temps_ecoule_s_operation
            return True

# Boucle de simulation de l'exécution de l'opération I/O active
while execution_io():
    pass

# Intégration du module de gestion I/O dans une simulation de système d'exploitation
os = {
    "name": "os_bac1_2025",
    "version": "v1.0",
    "modules": [md_io]
}

