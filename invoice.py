from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
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

    def print_receipt(self,receiptno,receiptpath,details):
        print(details)
        conn = self.get_config()
        print(conn)
        w, h = A4
        c = canvas.Canvas(receiptpath+"/"+str(receiptno) + ".pdf", pagesize=A4)

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
        desc1.textLine("Date : "+details[2]+"                   Receipt No : "+str(details[1]))
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

        # head11 = c.beginText(250, h - 490)
        # head11.setFont("Helvetica-Bold", 14)
        # c.line(50, h - 475, 550, h - 475)
        # head11.textLine(conn['hospitalname'])
        # # c.drawString(290, h - 510, conn['address'])
        # c.drawString(200, h - 510, conn['address'] + conn['city']+" - "+conn['pincode'])
        # c.line(50, h - 525, 550, h - 525)
        # c.drawText(head11)
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
        desc12.textLine("Date : " + details[2] + "                   Receipt No : " + str(details[1]))
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
        c.showPage()
        c.save()

    def str_list(self,inp):
        out = unquote(inp)
        out1 = re.sub("(.{80})", "\\1\n", out, 0, re.DOTALL)
        out_list = out1.splitlines()
        return out_list

    def print(self, details):
        print(details)
        w, h = A4
        c = canvas.Canvas("dischargesummary.pdf", pagesize=A4)
        c.drawImage('kh_head.png', 75, 750, width=400, height=75)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(55, h - 100, 'DISCHARGE SUMMARY/TREATMENT SUMMARY/DISCHARGE AT REQUEST/AGAINST MEDICAL ADVISE' )
        c.line(55, h - 105, 555, h - 105)
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - 125, 'Patient Name : ' )
        c.setFont('Helvetica', 12)
        c.drawString(150, h - 125,details['pname'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(300, h - 125, 'Age : ')
        c.setFont('Helvetica', 12)
        c.drawString(340, h - 125, details['age'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(450, h - 125, 'Sex : ')
        c.setFont('Helvetica', 12)
        c.drawString(490, h - 125, details['sex'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - 150, 'Date of Admission : ')
        c.setFont('Helvetica', 12)
        c.drawString(175, h - 150, details['doa'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(250, h - 150, 'Date of Discharge : ')
        c.setFont('Helvetica', 12)
        c.drawString(370, h - 150, details['dod'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(450, h - 150, 'Room No : ')
        c.setFont('Helvetica', 12)
        c.drawString(515, h - 150, details['roomno'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - 175, 'Consulted Doctor : ')
        c.setFont('Helvetica', 12)
        c.drawString(175, h - 175, details['cdr'])
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - 200, 'DIAGNOSIS : ')
        c.setFont('Helvetica', 12)
        x = 75
        y = 200
        dig = self.str_list(details['diagnosis'])
        for i in range(len(dig)):
            y += 18
            c.drawString(x, h - y, dig[i])
        print(y)

        pilly = 325
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - pilly, 'H/O PRESENT ILLNESS : ')
        c.setFont('Helvetica', 12)
        pill = self.str_list(details['pill'])
        for i in range(len(pill)):
            pilly += 18
            c.drawString(x, h - pilly, pill[i])
        print(pilly)

        milly = 450
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - milly, 'CO-MORBIT ILLNESS : ')
        c.setFont('Helvetica', 12)
        mill = self.str_list(details['mill'])
        for i in range(len(mill)):
            milly += 18
            c.drawString(x, h - milly, mill[i])
        print(milly)

        phy = 525
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - phy, 'PAST HISTORY : ')
        c.setFont('Helvetica', 12)
        pasthist = self.str_list(details['pasthist'])
        for i in range(len(pasthist)):
            phy += 18
            c.drawString(x, h - phy, pasthist[i])
        print(phy)

        fhy = 600
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - fhy, 'FAMILY HISTORY : ')
        c.setFont('Helvetica', 12)
        famhist = self.str_list(details['famhist'])
        for i in range(len(famhist)):
            fhy += 18
            c.drawString(x, h - fhy, famhist[i])
        print(fhy)

        cexy = 675
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - cexy, 'CLINICAL EXAMINATION : ')
        c.setFont('Helvetica', 12)
        cliex = self.str_list(details['cliex'])
        for i in range(len(cliex)):
            cexy += 18
            c.drawString(x, h - cexy, cliex[i])
        print(cexy)
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
        print(invy)

        cihy = 150
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - cihy, 'COURSE IN THE HOSPITAL : ')
        c.setFont('Helvetica', 12)
        cih = self.str_list(details['cih'])
        for i in range(len(cih)):
            cihy += 18
            c.drawString(x, h - cihy, cih[i])
        print(cihy)

        cady = 275
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - cady, 'CONDITION AT DISCHARGE : ')
        c.setFont('Helvetica', 12)
        cad = self.str_list(details['cih'])
        for i in range(len(cad)):
            cady += 18
            c.drawString(x, h - cady, cad[i])
        print(cady)

        diay = 400
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - diay, 'DISCHARGE ADVICE : ')
        c.setFont('Helvetica', 12)
        dia = self.str_list(details['da'])
        for i in range(len(dia)):
            diay += 18
            c.drawString(x, h - diay, dia[i])
        print(diay)

        revy = 580
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - revy, 'REVIEW : ')
        c.setFont('Helvetica', 12)
        review = self.str_list(details['review'])
        for i in range(len(review)):
            revy += 18
            c.drawString(x, h - revy, review[i])
        print(revy)

        umcy = 655
        c.setFont('Helvetica-Bold', 12)
        c.drawString(55, h - umcy, 'IF PRESENCE IF FOLLOWING SYMPTOMS SEEK URGENT MEIDCAL CARE : ')
        c.setFont('Helvetica', 12)
        umc = self.str_list(details['umc'])
        for i in range(len(umc)):
            umcy += 18
            c.drawString(x, h - umcy, umc[i])
        print(umcy)

        c.setFont('Helvetica-Bold', 12)
        c.drawString(400, h -775,"Doctor's Signature")

        c.showPage()
        c.save()


