# coding=utf-8

import  os
import  json
import  unicodecsv
import  gspread

# FIXME: see https://github.com/google/oauth2client/issues/401
# SignedJwtAssertionCredentials has been removed
# from    oauth2client.client import SignedJwtAssertionCredentials



def googleSpreadSheetToCSVFiles(credentialsJsonFile, spreadSheetKey, outputDirectory):
    json_key = json.load(open(credentialsJsonFile))
    scope = ['https://spreadsheets.google.com/feeds']
    # FIXME: see https://github.com/google/oauth2client/issues/401
    #  SignedJwtAssertionCredentials has been removed
    raise NotImplementedError('FIXME: see https://github.com/google/oauth2client/issues/401')
    credentials = SignedJwtAssertionCredentials(
        json_key['client_email'],
        json_key['private_key'],
        scope)
    connection = gspread.authorize(credentials)
    spreadsheet = connection.open_by_key(spreadSheetKey)
    generated_files = []
    for sheet in spreadsheet.worksheets():
        output_filename = os.path.join(outputDirectory, sheet.title+'.csv')
        with open(output_filename,'wb') as f:
            writer = unicodecsv.writer(f, encoding='utf-8')
            writer.writerows(sheet.get_all_values())
        generated_files.append(output_filename)
    return generated_files



if __name__ == '__main__':

    CREDENTIALS = '/media/jmfavre/Windows/D/PERSO-LOCAL/CERTIFICATS/GoogleScribesBot-ad1ea8e69715.json'
    SPREADSHEET = '1IdEOgB2a8qaohPqLuMgPdoxPTF7rrxnN4Tof8J7I2CI'
    DIR='.'
    print 'Transforming %s to csv file in %s ' % (SPREADSHEET,DIR)
    files = googleSpreadSheetToCSVFiles(CREDENTIALS, SPREADSHEET, DIR)
    print 'Generated files:', files