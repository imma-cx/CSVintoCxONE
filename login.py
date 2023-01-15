# define which environment to use
import auth.creds
import auth.authHeaders as authHeaders
import auth.authHeaders_sch as authHeaders_sch
import auth.authHeaders_prod as authHeaders_prod
import auth.creds as creds
import fromCSVtoJSON

environment = input("Which environment? ")

def __login(environment):
    
    customer = input("Customer name (N for None): ")
    if customer == 'N':
        customer == ""
    else:
        file_path_customer = "output/" + customer + "/"
        csv_data_customer = "data/" + customer + "/adidas_wout_filters.csv"

    #try:
    if environment == 'Canary':
        file_path = "/outputs"
        auth_headers_can = authHeaders.update_auth_headers
        print(authHeaders.__response)

    if environment == 'Schroders':
        server_url = creds.server_url_sch
        tenant = creds.tenant_sch
        auth_headers = authHeaders_sch.auth_headers_sch
        iam_url = creds.iam_url_sch
        file_path = "output/schroders/"

    if environment == 'Production':
        server_url = creds.server_url_prod
        tenant = creds.tenant_prod
        auth_headers = authHeaders_prod.auth_headers_prod
        iam_url = creds.iam_url_prod
        file_path = "output/production/"

__login(environment)


def __get_data_from_csv(customer):
    fromCSVtoJSON(customer) 