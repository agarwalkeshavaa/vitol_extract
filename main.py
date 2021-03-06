import os
import pytesseract
from pdf2image import convert_from_path
import uuid
import csv
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

try:
    from PIL import Image
except ImportError:
    import Image

tot_data=[['Name', 'Reg. No', 'Subject', 'Marks', 'Cert_ID', 'Grade']]
check_again=[['Path to File']]
cert_ID=[]
duplicate_cert=[['Reg. no', 'Cert_ID']]
# Details from the certificate in a class
class details:
    def __init__(self, name, reg_num, subject, marks, cert_id):
        """
        Creates the class for details

        Args:
            name (str): Name in the certificate
            reg_num (str): Reg. number
            marks (int): Marks obtained
            cert_id (str): Certificate ID generated with the certificate
        """
        self.name=name
        self.reg_no=reg_num
        self.marks=marks
        self.cert_id=cert_id
        self.subject = subject
        self.grade=grade(self.marks)
        if isDuplicate(self.cert_id):
            duplicate_cert.append([self.reg_no, self.cert_id, self.subject])
        else:
            tot_data.append([self.name, self.reg_no, self.subject, self.marks, self.cert_id, self.grade])

def grade(marks):
    """
    Assigns a grade according to the Marks Obtained

    Args:
        marks ([int]): [Marks Obtained from the certificate]

    Returns:
        [str]: [Grade for the subject]
    """
    if marks>=90:
        return 'S'
    elif marks>=80 and marks<90:
        return 'A'
    elif marks>=70 and marks<80:
        return 'B'
    elif marks >= 60 and marks<70:
        return 'C'
    elif marks >= 50 and marks<60:
        return 'D'
    else:
        return 'F'

def isDuplicate(cert):
    if not cert in cert_ID:
        cert_ID.append(cert)
        return False
    return True

def extract(path):
    """
    converts the PDF to Image file and Performs OCR and extracts the details

    Args:
        path (str): Path of the folder containing the pdf files
    """
    pages = convert_from_path(path, 500)
    for page in pages:
        img_path=str(uuid.uuid1())+'.jpg'
        page.save(img_path, 'JPEG')
    text=pytesseract.image_to_string(Image.open(img_path))
    os.remove(img_path)
    text_lines=[i for i in text.split('\n') if i!='' and i!=" "]
    if text_lines==[]:
        check_again.append([path])
        return
    cert_id=[i for i in text_lines if 'ID' in i][0].split(':')[1].split(' ')[1]
    marks=int([i for i in text_lines if 'consolidated' in i][0].split(' ')[-1][1:3])
    name=[text_lines.index(i) for i in text_lines if 'COMPLETION' in i]
    subject = text_lines[name[0]+4]
    name, reg_num=text_lines[name[0]+1], text_lines[name[0]+2]
    p1=details(name, reg_num, subject, marks, cert_id)

def files(path):
    """
    Gets the list of all the files

    Args:
        path (str): Path to the folder

    Returns:
        list: list of all the files
    """
    files_list=[]
    for root, dirs, files in os.walk(path):
        for filename in files:
            files_list.append(filename)
    return files_list

def write_to_csv(path, data_list):
    """Generate csv file."""
    with open(path, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_list)

if __name__ == '__main__':
    path = input("Path to the folder : ")
    files_lis=files(path)
    for _ in files_lis:
        #loop over all the files and write them to the csv file.
        tot_path= path+'/'+ _
        extract(tot_path)
    write_to_csv('Details.csv', tot_data)
    write_to_csv('Check_again.csv', check_again)
    write_to_csv('Duplicates.csv', data_list= duplicate_cert)