import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app.reports.statistical_report import StatisticalReport
from app.reports.detailed_report import DetailedReport

if __name__ == "__main__":
    sr = StatisticalReport()
    dr = DetailedReport()
    
    sr.generate_statistical_report()
    dr.generate_detailed_report()
