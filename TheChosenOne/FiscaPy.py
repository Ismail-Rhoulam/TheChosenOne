class FiscaAuto:

    # Automatisation de l'ir
    class ImpotSurRevenu:
        """
        Ici la variable barem accepte deux valeurs annuel et mensuel
        """
        vbi_annuel = ['A', 'a', 'Annuel', 'annuel']
        vbi_mensuel = ['M', 'm', 'Mensuel', 'mensuel']
        
        def __init__(self):
            self.salaire_de_base = input("Salaire de base: ") or 200000
            self.prime_ancien = input("Prime d'ancienneté: ") or 20000
            self.prime_produc = input("Prime de productivité: ") or 30000
            self.prime_panier = input("Prime de panier: ") or 12000
            self.prs_en_charge = input("Personne en charge: ") or 7
            self.barem = input("Annuel ou mensuel: ") or 'A'
            self.salaire_brut_global = int(self.salaire_de_base) + int(self.prime_ancien) + int(self.prime_produc) + int(self.prime_panier)

        def ir(self):
            self.salaire_brut_imposable = self.salaire_brut_global - int(self.prime_panier)

            cnss_max = 6000 * 0.0448 if self.barem in self.vbi_mensuel else 72000 * 0.0448
            cnss_mt = min(self.salaire_brut_imposable * 0.0448, cnss_max)
            amo_mt = self.salaire_brut_imposable * 0.0226
            b_abattement = 6500 if self.barem in self.vbi_mensuel else 78000
            abattement_max = 2916.67 if self.barem in self.vbi_mensuel else 35000
            abattement_ratio = 0.35 if self.salaire_brut_imposable >= b_abattement else 0.25
            abattement = min(self.salaire_brut_imposable * abattement_ratio, abattement_max)
            self.deduction = cnss_mt + amo_mt + abattement
            self.ded = cnss_mt + amo_mt

            self.salaire_net_imposable = self.salaire_brut_imposable - self.deduction

            if self.barem in self.vbi_mensuel:
                if self.salaire_net_imposable > 15000:
                    self.ir_brut = self.salaire_net_imposable * 0.38 - 2033.33
                elif self.salaire_net_imposable > 6666:
                    self.ir_brut = self.salaire_net_imposable * 0.34 - 1433.33
                elif self.salaire_net_imposable > 5000:
                    self.ir_brut = self.salaire_net_imposable * 0.3 - 1166.67
                elif self.salaire_net_imposable > 4166:
                    self.ir_brut = self.salaire_net_imposable * 0.2 - 666.67
                elif self.salaire_net_imposable > 2500:
                    self.ir_brut = self.salaire_net_imposable * 0.1 - 250
                else:
                    self.ir_brut = 0

            else:
                if self.salaire_net_imposable > 180000:
                    self.ir_brut = self.salaire_net_imposable * 0.38 - 24400
                elif self.salaire_net_imposable > 80000:
                    self.ir_brut = self.salaire_net_imposable * 0.34 - 17200
                elif self.salaire_net_imposable > 60000:
                    self.ir_brut = self.salaire_net_imposable * 0.3 - 14000
                elif self.salaire_net_imposable > 50000:
                    self.ir_brut = self.salaire_net_imposable * 0.2 - 8000
                elif self.salaire_net_imposable > 30000:
                    self.ir_brut = self.salaire_net_imposable * 0.1 - 3000
                else:
                    self.ir_brut = 0

            impu_fam = 30 if self.barem in self.vbi_mensuel else 360
            charge_max = min(int(self.prs_en_charge), 6)
            self.impu_mt = impu_fam * charge_max

            if self.ir_brut == 0:
                self.ir_net = 0
            else:
                self.ir_net = self.ir_brut - self.impu_mt

            return self.ir_net
        
        def salaire_net(self):
            self.ir()
            self.salaire_net_payer = self.salaire_brut_global - self.ded - self.ir_net
            if self.barem in self.vbi_mensuel:
                self.salaire_net_payer_m = self.salaire_net_payer
                self.salaire_net_payer_a = self.salaire_net_payer_m * 12
                return f"Salaire net annuel a payer est de {round(self.salaire_net_payer_a)} MAD\nSalaire net mensuel a payer est de {round(self.salaire_net_payer_m)} MAD"
            else:
                self.salaire_net_payer_a = self.salaire_net_payer
                self.salaire_net_payer_m = self.salaire_net_payer_a / 12
                return f"Salaire net annuel a payer est de {round(self.salaire_net_payer_a)} MAD\nSalaire net mensuel a payer est de {round(self.salaire_net_payer_m)} MAD"
            
        def __str__(self):
            b = "Annuel" if self.barem in self.vbi_annuel else "Mensuel"
            data = [
                ["Salaire de base", f'{self.salaire_de_base} MAD'],
                ["Prime d'ancienneté", f'{self.prime_ancien} MAD'],
                ["Prime de productivité", f'{self.prime_produc} MAD'],
                ["Prime de panier", f'{self.prime_panier} MAD'],
                ["Salaire brut global", f'{self.salaire_brut_global} MAD'],
                ["Bulletin de paie", b],
                ["Nombre de personne en charge", f'{self.prs_en_charge} personnes']
            ]

            width = max(len(row[0]) for row in data)
            
            table_str = ""
            for row in data:
                table_str += row[0].ljust(width) + "    " + row[1] + "\n"
    
            return table_str
        
        def resultats(self):
            self.ir()
            self.salaire_net()
            data = [
                ["Total des exoneration", f'{self.salaire_brut_global - self.salaire_brut_imposable} MAD'],
                ["Salaire brut imposable", f'{self.salaire_brut_imposable} MAD'],
                ["Deduction", f'{round(self.deduction, 2)} MAD'],
                ["Salaire net imposable", f'{round(self.salaire_net_imposable, 2)} MAD'],
                ["Impot sur revenu brut", f'{round(self.ir_brut, 2)} MAD'],
                ["Imputation charge de famille", f'{self.impu_mt} MAD'],
                ["Impot sur revenu net", f'{round(self.ir_net, 2)} MAD'],
                ["Salaire net a payer annuellement", f'{round(self.salaire_net_payer_a, 2)} MAD'],
                ["Salaire net a payer mensuellement", f'{round(self.salaire_net_payer_m, 2)} MAD']
                ]

            width = max(len(row[0]) for row in data)
            
            table_str = ""
            for row in data:
                table_str += row[0].ljust(width) + "    " + row[1] + "\n"
    
            return table_str
            



            