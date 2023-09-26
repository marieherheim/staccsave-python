import json
import matplotlib.pyplot as plt

class Account:

    def __init__(self, data):
        self.id = data['id']
        self.account_number = data['account_number']
        self.account_type = data['account_type']
        self.balance = data['balance']
        self.currency = data['currency']
        self.owner = data['owner']
        self.age = data['age']
        self.city = data['city']
        self.interest_rate = data['interest_rate']

    def age_range(self):
        if self.age <= 25:
            return '0-25'
        elif self.age <= 49:
            return '26-49'
        elif self.age <= 79:
            return '50-79'
        else:
            return '80-150'

class Bank:

    def __init__(self, accounts_data):
        self.accounts = [Account(data) for data in accounts_data]

    def get_account_by_id(self, account_id):
        for account in self.accounts:
            if account.id == account_id:
                return account
        return None

    def average_balance(self):
        return sum(account.balance for account in self.accounts) / len(self.accounts)

    def average_balance_for_age(self, age_range):
        balances = [account.balance for account in self.accounts if account.age_range() == age_range]
        return sum(balances) / len(balances) if balances else 0

    def average_balance_for_city(self, city):
        balances = [account.balance for account in self.accounts if account.city == city]
        return sum(balances) / len(balances) if balances else 0


class Interface:

    def __init__(self, bank):
        self.bank = bank

    def main_menu(self):
        while True:
            print("\nHei og velkommen til StaccSave! \n Vennligst velg ett av følgende alternativer:")
            print("1. For å logge inn, trykk 1")
            print("2. For å avslutte, trykk 2 \n")
            choice = input()

            if choice == '1':
                account_id = input("Vennligst skriv inn din brukerID (accXXX): ")
                # Setter brukeren til å være den brukeren fra datasettet med lik ID som input.
                account = self.bank.get_account_by_id(account_id.lower()) # Bruker .lower() for å unngå at stor bokstav hindrer innlogging.
                # Åpner account menu for riktig bruker, ved å gi riktig bruker som argument til account_menu metoden.
                if account:
                    self.account_menu(account)
                # Hvis det er skrevet feil brukerID/en brukerID som ikke finnes så kommer det feilmelding og du sendes tilbake til start.
                else:
                    print("Invalid userID!")
            elif choice == '2':
                break

    def account_menu(self, account):
        while True:
            print(f"\nHva ønsker du å gjøre i dag, {account.owner}?")
            print("1. Se din saldo")
            print("2. Sammenlign din sparing")
            print("3. Sparekalkulator")
            print("4. Sett et sparemål")
            print("5. Se graf: Sammenlign din sparing")
            print("6. Se graf: Nåværende vs. Ønsket sparemål")
            print("7. Gå tilbake")

            choice = input()

            if choice == '1':
                self.view_balance(account)
            elif choice == '2':
                self.compare_savings(account)
            elif choice == '3':
                self.calculate_savings(account)
            elif choice == '4':
                self.saving_goal(account)
            elif choice == '5':
                self.saving_graph1(account)
            elif choice == '6':
                self.saving_graph2(account)
            elif choice == '7':
                break

    def saving_graph1(self, account):

        # Graf 1: Sammenligning din sparing med andre:

        # Legger inn dataen som skal brukes i grafen
        labels = [f'{account.owner}', 'Alle kunder', f'Din aldersgruppe', f'{account.city}']
        values = [
            account.balance,
            self.bank.average_balance(),
            self.bank.average_balance_for_age(account.age_range()),
            self.bank.average_balance_for_city(account.city)
        ]

        # Lager selve grafen
        plt.bar(labels, values, color=['blue', 'green', 'red', 'purple'])
        plt.ylabel(f'{account.currency}')
        plt.title(f'Din sparing vs. andres sparing')
        plt.show()

    def saving_graph2(self, account):
        # Graf 2: Sammenlign din saldo i årene fremover med hva du kunne ha hatt med mer sparing:

        current_monthly_savings = float(input("Hvor mye sparer du per måned nå? "))
        desired_monthly_savings = float(input("Hvor mye ønsker du å spare i stedet? "))

        years = 20
        r = account.interest_rate
        current_projections = [account.balance]
        desired_projections = [account.balance]

        # Utregning av forventet vekst
        for year in range(1, years + 1):
            current_balance = current_projections[-1] + 12 * current_monthly_savings
            desired_balance = desired_projections[-1] + 12 * desired_monthly_savings

            current_balance *= (1 + r)
            desired_balance *= (1 + r)

            current_projections.append(current_balance)
            desired_projections.append(desired_balance)

        # Utfylling av grafen
        plt.figure()
        plt.plot(range(years + 1), current_projections, label="Nåværende sparing", color="purple")
        plt.plot(range(years + 1), desired_projections, label="Ønsket sparing", color="green")
        plt.xlabel('År')
        plt.ylabel(f'{account.currency}')
        plt.title(f'Nåværende og ønsket sparing for {account.owner} over {years} år.')
        plt.legend()
        plt.show()


    def saving_goal(self, account):
        goal_amount = float(input("Hvor mye ønsker du å spare? Skriv inn et beløp: "))
        duration = int(input("Om hvor mange måneder ønsker du å ha nådd ditt sparemål? Skriv inn antall måneder: "))

        required_monthly_saving = (goal_amount - account.balance) / duration
        print(
            f"For å nå ditt sparemål om {duration} måneder, så må du spare {required_monthly_saving:.2f} {account.currency} kr i måneden.")


    def view_balance(self, account):
        print(f"Din nåværende saldo er: {round(account.balance)} {account.currency}")

    def compare_savings(self, account):

        print("------------------ Sammenligning av deg vs. alle våre kunder: ------------------")
        print(f"Din saldo er: {round(account.balance)} kr, gjennomsnittlig saldo for alle våre kunder er: {round(self.bank.average_balance())} kr.")

        if account.balance > self.bank.average_balance():
            print("Du har spart mer enn gjennomsnittet, bra jobba!")
        elif account.balance == self.bank.average_balance():
            print("Du sparer like mye som gjennomsnittet.\nPrøv vårt budjsettverktøy for å se hvordan du kan spare mer!")
        else:
            print(f"Du har spart {round(self.bank.average_balance()-account.balance)} kr mindre enn gjennomsnittet blant våre kunder. \n")

        print("------------------ Sammenligning med andre på din alder: ------------------")
        print(f"Din saldo er: {round(account.balance)} kr, andre i din aldersgruppe ({account.age_range()}) har en gjennomsnittlig saldo på: {round(self.bank.average_balance_for_age(account.age_range()))} kr.\n")

        if account.balance > self.bank.average_balance_for_age(account.age_range()):
            print("Du har spart mer enn gjennomsnittet for din aldersgruppe, bra jobba!")
        elif account.balance == self.bank.average_balance_for_age(account.age_range()):
            print("Du sparer like mye som gjennomsnittet for din aldersgruppe.\n")
        else:
            print(f"Du har spart {round(self.bank.average_balance_for_age(account.age_range())-account.balance)} kr mindre enn gjennomsnittet for din aldersgruppe. \n")

        print(f"------------------ Sammenligning med andre i {account.city}: ------------------")
        print(f"Din saldo er: {round(account.balance)} kr, andre i {account.city} har en gjennomsnittlig saldo på: {round(self.bank.average_balance_for_city(account.city))} kr.\n")

        if account.balance > self.bank.average_balance_for_city(account.city):
            print(f"Du har spart mer enn gjennomsnittet i {account.city}, bra jobba!")
        elif account.balance == self.bank.average_balance_for_city(account.city):
            print(f"Du sparer like mye som gjennomsnittet i {account.city}.\n")
        else:
            print(f"Du har spart {round(self.bank.average_balance_for_city(account.city)-account.balance)} kr mindre enn gjennomsnittet i {account.city}.\n")

    def calculate_savings(self, account):
        years = int(input("Skriv inn antall år du ønsker å spare: \n"))
        b = account.balance
        r = account.interest_rate
        n = 1

        print(f"\nMed din årlige rente på {100*account.interest_rate}% så vil din saldo de neste {years} årene være:")
        for year in range(1, years + 1):
            a = b * (1 + r / n) ** (n * year)
            print(f"Din saldo vil være på: {a:.2f} kr om {year} år.")



with open("accounts.json", "r") as file:
    data = json.load(file)

bank = Bank(data['accounts'])
interface = Interface(bank)
interface.main_menu()
