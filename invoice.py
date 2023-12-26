from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Image
import json
import re
from urllib.parse import unquote
import os
path = os.getcwd()
app_path = os.path.abspath(os.path.join(path, os.pardir))

class receipt:
    def get_config(self):
        jsonfilepath = r"" + path + "/config.json"
        with open(jsonfilepath, 'r') as _:
            jsonbody = json.load(_)
        return jsonbody

    def print_receipt(self,receiptpath,details):
        # print(details)
        conn = self.get_config()
        w, h = A4
        c = canvas.Canvas(receiptpath+"/opd.pdf", pagesize=A4)
        # head = c.beginText(250, h - 100)
        # head.setFont("Helvetica-Bold", 14)
        # c.line(50, h - 85, 550, h - 85)
        # head.textLine(conn['hospitalname'])
        # # c.drawString(290, h - 115, conn['address'])
        # c.drawString(200, h - 115, conn['address'] + conn['city']+" - "+conn['pincode'])
        # c.line(50, h - 135, 550, h - 135)
        # c.drawText(head)
        c.line(55, h - 50, 555, h - 50)
        c.drawImage('kh_head.png', 100, h - 130, width=400, height=75)
        c.line(55, h - 130, 555, h - 130)
        op = c.beginText(225, h - 155)
        op.setFont("Helvetica-Bold", 13)
        op.textLine("OUT PATIENT RECEIPT")
        c.drawText(op)
        desc = c.beginText(60, h - 175)
        desc.setFont("Helvetica", 12)
        desc.textLine("Token No : "+str(details[0]))
        desc.textLine("Patient Name : "+details[4])
        desc.textLine("Age : "+str(details[5])+"      Sex : "+details[6])
        desc.textLine("Phone : "+details[9])
        c.drawText(desc)
        desc1 = c.beginText(260, h - 175)
        desc1.setFont("Helvetica", 12)
        desc1.textLine("Date : "+details[2]+"                Receipt No : "+str(details[1]))
        desc1.textLine("Time : 11:23:45")
        desc1.textLine("Place : "+details[8])
        desc1.textLine("Consulting Doctor : "+details[10])
        c.line(50, h - 265, 550, h - 265)
        c.drawText(desc1)
        c.drawString(100, h - 255,
                     "sl.no                                       Particulars                                   Amount")
        # c.line(50, h - 290, 550, h - 290)
        c.drawString(100, h - 285,
                     "  1.                          Consultation Fees                                      Rs. "+str(details[12]))
        c.line(50, h - 335, 550, h - 335)
        c.drawString(55, h - 350, "printedby: "+details[14])


        c.line(55, h - 440, 555, h - 440)
        c.drawImage('kh_head.png', 100, h - 520, width=400, height=75)
        c.line(55, h - 520, 555, h - 520)

        op11 = c.beginText(225, h - 555)
        op11.setFont("Helvetica-Bold", 13)
        op11.textLine("OUT PATIENT RECEIPT")
        c.drawText(op11)
        desc11 = c.beginText(60, h - 575)
        desc11.setFont("Helvetica", 12)
        desc11.textLine("Token No : " + str(details[0]))
        desc11.textLine("Patient Name : " + details[4])
        desc11.textLine("Age : " + details[5] + "      Sex : " + details[6])
        desc11.textLine("Phone : " + details[9])
        c.drawText(desc11)
        desc12 = c.beginText(260, h - 575)
        desc12.setFont("Helvetica", 12)
        desc12.textLine("Date : " + details[2] + "                Receipt No : " + str(details[1]))
        desc12.textLine("Time : 11:23:45")
        desc12.textLine("Place : " + details[8])
        desc12.textLine("Consulting Doctor : " + details[10])
        c.line(50, h - 635, 550, h - 635)
        c.drawText(desc12)
        c.drawString(100, h - 655,
                     "sl.no                                       Particulars                                   Amount")
        c.line(50, h - 660, 550, h - 660)
        c.drawString(100, h - 685,
                     "  1.                          Consultation Fees                                      Rs. "+str(details[12]))
        c.line(50, h - 735, 550, h - 735)
        c.drawString(55, h - 750, "printedby: " + details[14])
        c.showPage()
        c.save()

    def str_list(self,inp):
        out = unquote(inp)
        out1 = re.sub("(.{80})", "\\1\n", out, 0, re.DOTALL)
        out_list = out1.splitlines()
        return out_list

    def print_discharge_summary(self, details):
        # print(details)
        w, h = A4
        c = canvas.Canvas("dischargesummary.pdf", pagesize=A4)
        c.drawImage('kh_head.png', 75, 750, width=400, height=75)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(55, h - 100, 'DISCHARGE SUMMARY/TREATMENT SUMMARY/DISCHARGE AT REQUEST/AGAINST MEDICAL ADVISE' )
        c.line(55, h - 105, 555, h - 105)
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - 125, 'IPD No : ')
        c.setFont('Helvetica', 12)
        c.drawString(110, h - 125, details['ipdno'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(200, h - 125, 'Patient Name : ' )
        c.setFont('Helvetica', 12)
        c.drawString(290, h - 125,details['pname'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(410, h - 125, 'Age : ')
        c.setFont('Helvetica', 12)
        c.drawString(440, h - 125, details['age'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(470, h - 125, 'Sex : ')
        c.setFont('Helvetica', 12)
        c.drawString(510, h - 125, details['sex'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - 150, 'Date of Admission : ')
        c.setFont('Helvetica', 12)
        c.drawString(175, h - 150, details['doa'].replace("%3A" , ":"))
        c.setFont('Helvetica-Bold', 12)
        c.drawString(310, h - 150, 'Date of Discharge : ')
        c.setFont('Helvetica', 12)
        c.drawString(430, h - 150, details['dod'].replace("%3A" , ":"))
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - 175, 'Room No : ')
        c.setFont('Helvetica', 12)
        c.drawString(120, h - 175, details['roomno'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(150, h - 175, 'Consulted Doctor : ')
        c.setFont('Helvetica', 12)
        c.drawString(275, h - 175, details['cdr'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - 200, 'DIAGNOSIS : ')
        c.setFont('Helvetica', 12)
        x = 75
        y = 200
        dig = self.str_list(details['diagnosis'])
        for i in range(len(dig)):
            y += 18
            c.drawString(x, h - y, dig[i])
        # print(y)
        pilly = 325
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - pilly, 'H/O PRESENT ILLNESS : ')
        c.setFont('Helvetica', 12)
        pill = self.str_list(details['pill'])
        for i in range(len(pill)):
            pilly += 18
            c.drawString(x, h - pilly, pill[i])
        # print(pilly)
        milly = 450
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - milly, 'CO-MORBIT ILLNESS : ')
        c.setFont('Helvetica', 12)
        mill = self.str_list(details['mill'])
        for i in range(len(mill)):
            milly += 18
            c.drawString(x, h - milly, mill[i])
        # print(milly)
        phy = 525
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - phy, 'PAST HISTORY : ')
        c.setFont('Helvetica', 12)
        pasthist = self.str_list(details['pasthist'])
        for i in range(len(pasthist)):
            phy += 18
            c.drawString(x, h - phy, pasthist[i])
        # print(phy)
        fhy = 600
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - fhy, 'FAMILY HISTORY : ')
        c.setFont('Helvetica', 12)
        famhist = self.str_list(details['famhist'])
        for i in range(len(famhist)):
            fhy += 18
            c.drawString(x, h - fhy, famhist[i])
        # print(fhy)
        cexy = 675
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - cexy, 'CLINICAL EXAMINATION : ')
        c.setFont('Helvetica', 12)
        cliex = self.str_list(details['cliex'])
        for i in range(len(cliex)):
            cexy += 18
            c.drawString(x, h - cexy, cliex[i])
        # print(cexy)
        c.showPage()
        #Page 2
        invy = 75
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h -invy, 'INVESTIGATION : ')
        c.setFont('Helvetica', 12)
        invest = self.str_list(details['invest'])
        for i in range(len(invest)):
            invy += 18
            c.drawString(x, h -invy, invest[i])
        # print(invy)
        cihy = 150
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - cihy, 'COURSE IN THE HOSPITAL : ')
        c.setFont('Helvetica', 12)
        cih = self.str_list(details['cih'])
        for i in range(len(cih)):
            cihy += 18
            c.drawString(x, h - cihy, cih[i])
        # print(cihy)
        cady = 275
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - cady, 'CONDITION AT DISCHARGE : ')
        c.setFont('Helvetica', 12)
        cad = self.str_list(details['cih'])
        for i in range(len(cad)):
            cady += 18
            c.drawString(x, h - cady, cad[i])
        # print(cady)
        diay = 400
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - diay, 'DISCHARGE ADVICE : ')
        c.setFont('Helvetica', 12)
        dia = self.str_list(details['da'])
        for i in range(len(dia)):
            diay += 18
            c.drawString(x, h - diay, dia[i])
        # print(diay)
        revy = 580
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - revy, 'REVIEW : ')
        c.setFont('Helvetica', 12)
        review = self.str_list(details['review'])
        for i in range(len(review)):
            revy += 18
            c.drawString(x, h - revy, review[i])
        # print(revy)
        umcy = 655
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - umcy, 'IF PRESENCE IF FOLLOWING SYMPTOMS SEEK URGENT MEIDCAL CARE : ')
        c.setFont('Helvetica', 12)
        umc = self.str_list(details['umc'])
        for i in range(len(umc)):
            umcy += 18
            c.drawString(x, h - umcy, umc[i])
        # print(umcy)
        c.setFont('Helvetica-Bold', 12)
        c.drawString(400, h -775,"Doctor's Signature")
        c.setFont('Helvetica', 10)
        c.drawString(55, h - 790, "printedby: " + details['user'])
        c.showPage()
        c.save()

    def print_admissionform(self,receiptno,receiptpath,details):
        # print(details)
        # print(details['user'])
        w, h = A4
        c = canvas.Canvas("admissionform.pdf", pagesize=A4)
        c.drawImage('kh_head.png', 75, 750, width=400, height=75)
        c.setFont('Helvetica-Bold', 16)
        c.drawString(200, h - 125, 'IN PATIENT ADMISSION FORM')
        c.line(55, h - 130, 555, h - 130)
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 175, 'IPD no : ')
        c.setFont('Helvetica', 12)
        c.drawString(125, h - 175, details['ipdno'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(325, h - 175, 'Patient Name : ')
        c.setFont('Helvetica', 12)
        c.drawString(410, h - 175, details['patient'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 225, 'Date of Admission : ')
        c.setFont('Helvetica', 12)
        c.drawString(195, h - 225, details['doa'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(325, h - 225, 'Age : ')
        c.setFont('Helvetica', 12)
        c.drawString(360, h - 225, details['age'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 275, 'Bloodgroup : ')
        c.setFont('Helvetica', 12)
        c.drawString(155, h - 275, details['bloodgroup'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(325, h - 275, 'Sex : ')
        c.setFont('Helvetica', 12)
        c.drawString(360, h - 275, details['sex'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 325, 'Room no : ')
        c.setFont('Helvetica', 12)
        c.drawString(140, h - 325, details['roomno'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(325, h - 325, 'Guardian : ')
        c.setFont('Helvetica', 12)
        c.drawString(390, h - 325, details['guardian'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 375, 'Contact no : ')
        c.setFont('Helvetica', 12)
        c.drawString(150, h - 375, details['mobileno'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(325, h - 375, 'Maritialstatus : ')
        c.setFont('Helvetica', 12)
        c.drawString(415, h - 375, details['maritialstatus'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 425, 'Consult Dr. : ')
        c.setFont('Helvetica', 12)
        c.drawString(150, h - 425, details['consultingdr'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(325, h - 425, 'Dept : ')
        c.setFont('Helvetica', 12)
        c.drawString(365, h - 425, details['department'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 475, 'Ref Dr. : ')
        c.setFont('Helvetica', 12)
        c.drawString(125, h - 475, details['referreddr'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 525, 'Present Comp : ')
        c.setFont('Helvetica', 12)
        c.drawString(170, h - 525, details['presentcomplaint'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 575, 'Family Hist : ')
        c.setFont('Helvetica', 12)
        c.drawString(150, h - 575, details['familyhistory'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 625, 'Remarks : ')
        c.setFont('Helvetica', 12)
        c.drawString(140, h - 625, details['remarks'])
        # c.setFont('Helvetica-Bold', 12)
        # c.drawString(75, h - 675, 'Advance : Rs. ')
        # c.setFont('Helvetica', 12)
        # c.drawString(155, h - 675, details['advance'])
        # c.setFont('Helvetica-Bold', 12)
        # c.drawString(325, h - 675, 'Payment Mode : ')
        # c.setFont('Helvetica', 12)
        # c.drawString(425, h - 675, details['paymentmode'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(400, h - 775, "Authority Signature")
        c.setFont('Helvetica', 10)
        c.drawString(55, h - 790, "printedby: "+details['user'])
        c.showPage()
        c.save()

    def print_discharge_bill(self, details):
        # print(details)
        w, h = A4
        c = canvas.Canvas("dischargebill.pdf", pagesize=A4)
        c.drawImage('kh_head.png', 75, 750, width=400, height=75)
        c.setFont('Helvetica-Bold', 16)
        c.drawString(240, h - 120, 'DISCHARGE BILL')
        c.line(55, h - 130, 555, h - 130)
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 155, 'IPD no : ')
        c.setFont('Helvetica', 12)
        c.drawString(125, h - 155, details['ipdno'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(325, h - 155, 'Patient Name : ')
        c.setFont('Helvetica', 12)
        c.drawString(410, h - 155, details['patient'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 180, 'Age : ')
        c.setFont('Helvetica', 12)
        c.drawString(110, h - 180, details['age'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(325, h - 180, 'Sex : ')
        c.setFont('Helvetica', 12)
        c.drawString(360, h - 180, details['sex'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 205, 'Room no : ')
        c.setFont('Helvetica', 12)
        c.drawString(140, h - 205, details['roomno'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(325, h - 205, 'Guardian : ')
        c.setFont('Helvetica', 12)
        c.drawString(390, h - 205, details['guardian'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 230, 'Date of Discharge : ')
        c.setFont('Helvetica', 12)
        c.drawString(195, h - 230, details['dod'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(325, h - 230, 'Date of Admission : ')
        c.setFont('Helvetica', 12)
        c.drawString(445, h - 230, details['doa'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 255, 'Contact no : ')
        c.setFont('Helvetica', 12)
        c.drawString(150, h - 255, details['contactno'])
        # c.setFont('Helvetica-Bold', 12)
        # c.drawString(325, h - 255, 'Advance : ')
        # c.setFont('Helvetica', 12)
        # c.drawString(390, h - 255, details['adv'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(75, h - 280, 'Consult Dr. : ')
        c.setFont('Helvetica', 12)
        c.drawString(150, h - 280, details['consdr'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(325, h - 280, 'Dept : ')
        c.setFont('Helvetica', 12)
        c.drawString(365, h - 280, details['dept'])
        c.line(55, h - 295, 555, h - 295)
        c.setFont('Helvetica', 12)
        if details['item1'] != 'None':
            c.drawString(100, h - 350, details['item1'].lstrip())
            c.drawString(400, h - 350, 'Rs.' + details['amt1'])
        if details['item2'] != 'None':
            c.drawString(100, h - 375, details['item2'].lstrip())
            c.drawString(400, h - 375, 'Rs.' + details['amt2'])
        if details['item3'] != 'None':
            c.drawString(100, h - 400, details['item3'].lstrip())
            c.drawString(400, h - 400, 'Rs.' + details['amt3'])
        if details['item4'] != 'None':
            c.drawString(100, h - 425, details['item4'].lstrip())
            c.drawString(400, h - 425, 'Rs.' + details['amt4'])
        if details['item5'] != 'None':
            c.drawString(100, h - 450, details['item5'].lstrip())
            c.drawString(400, h - 450, 'Rs.' + details['amt5'])
        if details['item6'] != 'None':
            c.drawString(100, h - 475, details['item6'].lstrip())
            c.drawString(400, h - 475, 'Rs.' + details['amt6'])
        if details['item7'] != 'None':
            c.drawString(100, h - 500, details['item7'].lstrip())
            c.drawString(400, h - 500, 'Rs.' + details['amt7'])
        if details['item8'] != 'None':
            c.drawString(100, h - 525, details['item8'].lstrip())
            c.drawString(400, h - 525, 'Rs.' + details['amt8'])
        c.line(55, h - 580, 555, h - 580)
        c.drawString(100, h - 600, "Total")
        c.drawString(400, h - 600, 'Rs.' + details['total'])
        c.line(55, h - 610, 555, h - 610)
        c.setFont('Helvetica-Bold', 12)
        c.drawString(400, h - 775, "Authority Signature")
        c.setFont('Helvetica', 10)
        c.drawString(55, h - 790, "printedby: " + details['user'])
        c.showPage()
        c.save()

    def print_dailycashreport(self,details):
        print(details[0])
        print(details[1])





