from backend import ReportMaker
# from gui import MainWindow

file_path = '/Users/saarim/git-local/nlc-app/sample-data.xlsx'
sys_lst = ['NSBS', 'SBS', 'TBS', 'MBS', 'BBS', 'LBS']
dump_path = '/Users/saarim/git-local/nlc-app/'
obj = ReportMaker(file_path, sys_lst, dump_path)
obj.start_process()