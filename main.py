from lib.Retrievers import DebtRetrieval
from lib.WorldBankDataRetriever import WorldBankDataRetriever


def all():
    retriever = [
        # AverageSalary("Average Salary OECD", ),
        # GiniCoefficientRetrieval("Gini coefficient", is_rate=True),
        # WorldBankDataRetriever("FI.RES.TOTL.CD"),
        # WorldBankDataRetriever("GB.XPD.RSDV.GD.ZS", is_rate=True,min_year_range=[1996,1997] ),
        # WorldBankDataRetriever("GC.XPN.TOTL.GD.ZS", is_rate=True, ),
        # WorldBankDataRetriever("IP.JRN.ARTC.SC", min_year_range=[1996,1997]),
        # WorldBankDataRetriever("NE.EXP.GNFS.ZS", is_rate=True),
        # WorldBankDataRetriever("NY.GDP.MKTP.CD"),
        # WorldBankDataRetriever("SE.XPD.TOTL.GB.ZS", is_rate=True),
        # WorldBankDataRetriever("SI.DST.10TH.10", min_year_range=[1996,1997]),
        # WorldBankDataRetriever("SI.POV.NAHC", is_rate=True, min_year_range=[2002,2003]),
        # WorldBankDataRetriever("SM.POP.NETM"),
        # WorldBankDataRetriever("SP.POP.0014.TO.ZS", is_rate=True),
        # WorldBankDataRetriever("SP.POP.1564.TO.ZS", is_rate=True),
        # WorldBankDataRetriever("SP.URB.TOTL"),
        # WorldBankDataRetriever("TX.VAL.MRCH.CD.WT"),
        # LaborPerHour("Output per hour worked", ),
        # WorldBankDataRetriever("EG.USE.ELEC.KH.PC"),
        DebtRetrieval("Debt as % of GDP", is_rate=True),
        WorldBankDataRetriever("EG.USE.COMM.FO.ZS", is_rate=True, ),
        WorldBankDataRetriever("EG.USE.PCAP.KG.OE"),
        WorldBankDataRetriever("GC.TAX.TOTL.GD.ZS", is_rate=True,  round=1),
        WorldBankDataRetriever("MS.MIL.XPND.GD.ZS", is_rate=True, round=1),
        WorldBankDataRetriever("NY.ADJ.NNTY.PC.KD", ),
        WorldBankDataRetriever("NY.GDP.PCAP.KN"),
        WorldBankDataRetriever("SH.ALC.PCAP.LI", min_year_range=[2000, 2001]),
        WorldBankDataRetriever("SH.MED.PHYS.ZS"),
        WorldBankDataRetriever("SL.GDP.PCAP.EM.KD"),
        WorldBankDataRetriever("SL.GDP.PCAP.EM.KD"),
        WorldBankDataRetriever("SL.TLF.TOTL.IN"),
        WorldBankDataRetriever("SM.POP.RHCR.EA", is_rate=True),
        WorldBankDataRetriever("SP.DYN.CBRT.IN", is_rate=True),
        WorldBankDataRetriever("SP.DYN.LE00.IN", is_rate=True),
        WorldBankDataRetriever("SP.POP.65UP.TO.ZS", is_rate=True),
        WorldBankDataRetriever("SP.POP.TOTL"),
        WorldBankDataRetriever("VC.IHR.PSRC.P5"),
    ]
    #WorldBankDataRetriever("VC.IHR.PSRC.P5").plot()
    for retriever_instance in retriever:
        retriever_instance.plot()



if __name__ == '__main__':
    all()
