import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import xlsxwriter
import os


def timePlus(time: dt.time, timedelta: dt.timedelta):
    start = dt.datetime(2000, 1, 1,
        hour=time.hour, minute=time.minute, second=time.second)
    end = start + timedelta
    return end.time()

def timeMinus(time: dt.time, timedelta: dt.timedelta):
    start = dt.datetime(2000, 1, 1,
        hour=time.hour, minute=time.minute, second=time.second)
    end = start - timedelta
    return end.time()

def toDatetime(date: dt.date, time: dt.time):
    return dt.datetime(date.year, date.month, date.day, time.hour, time.minute, time.second)


class parseExcel():
    def __init__(self, filepath: str, sys_list: list):
        self.filepath = filepath
        self.sys_list = sys_list
        
    def start_process(self):
        dataframe = self.load_dataframe()
        sys_map, idx_list = self.get_machine_count(dataframe, self.sys_list)
        print(sys_map)                  # test passed
        print(idx_list)                 # test passed
        mach_runtime = self.get_mach_runtime(idx_list, dataframe)
        print(mach_runtime[0][0])       # test passed
        sys_runtime = self.get_sys_runtime(idx_list, mach_runtime)
        print(sys_runtime[0])           # test passed
        max_size = 0
        for i in range(len(idx_list)):
            max_size = max(max_size, len(idx_list[i]))
        self.plot_runtime(sys_runtime, max_size)    # test passed
        start_arr, end_arr = self.get_sys_activity_status(sys_runtime)
        print(start_arr)                # test passed
        print(end_arr)                  # test passed

        

    def load_dataframe(self):
        assert self.filepath.endswith('.xlsx'), 'file must be in excel format'
        return pd.read_excel(self.filepath, header=None)

    def get_machine_count(self, df: pd.DataFrame, sys: list):
        """
        Returns a dictionary of the number of machines in each system
        and the list of starting index in the dataframe for each machine.
        :param df: DataFrame of machine running schedules
        :param sys: List of system names
        """
        idx_list = []
        sys_map = {}
        for i in range(len(df[0])):
            if type(df[0][i])==dt.time:
                df[0][i] = timeMinus(df[0][i], dt.timedelta(hours=6))
                df[1][i] = timeMinus(df[1][i], dt.timedelta(hours=6, seconds=1))
        for i in range(len(sys)):
            temp = []
            sys_map[sys[i]] = 0
            for j in range(len(df[0])):
                if df[0][j]==sys[i]:
                    temp.append(j)
                    sys_map[sys[i]]+=1
            idx_list.append(temp)
        return sys_map, idx_list

    def get_mach_runtime(self, idx_list: list, df: pd.DataFrame):
        """
        Returns a list of running status (1-> on, 0-> off) for each machine 
        at time intervals of 5 minutes.
        :param idx_list: List of starting index in the dataframe for each machine
        :param df: Dataframe of machine running schedules
        """
        l0 = []
        for sys_i in idx_list:
            l1 = []
            for mach_j in range(len(sys_i)):
                l2 = [1]*288
                idx = sys_i[mach_j]+1
                while(type(df[0][idx])==dt.time):
                    t0 = df[0][idx]
                    t1 = df[1][idx]
                    ts = (dt.datetime(2000,1,1,t0.hour,t0.minute,t0.second)
                            -dt.datetime(2000,1,1,0,0,0))/dt.timedelta(seconds=300)
                    te = (dt.datetime(2000,1,1,t1.hour,t1.minute,t1.second)
                            -dt.datetime(2000,1,1,0,0,0))/dt.timedelta(seconds=300)
                    start=int(ts)
                    end=int(te)
                    for i in range(start, end+1):
                        l2[i]=0
                    idx+=1
                l1.append(l2)
            l0.append(l1)
        return l0
    
    def get_sys_runtime(self, idx_list, runtime_list):
        """
        Returns a list of number of active machines in each system 
        at time interval of every 5 minutes.
        :param idx_list: List of starting index in the dataframe for each machine
        :param runtime_list: List of running status for each machine
        """
        l0 = []
        for i in range(len(self.sys_list)):
            l1 = []
            for j in range(288):
                t = 0
                for k in range(len(idx_list[i])):
                    t+=runtime_list[i][k][j]
                l1.append(t)
            l0.append(l1)
        return l0

    def plot_runtime(self, lst, _max):
        plt.rcParams["figure.figsize"] = (20,5)
        x = [(i/12)+6 for i in range(0,288)]
        fig, ax = plt.subplots()
        for i in range(len(self.sys_list)):
            ax.plot(x, lst[i])
        plt.xticks(list(range(6, 31)))
        plt.yticks(list(range(0, _max+2)))
        plt.show()

    def get_sys_activity_status(self, lst):
        """
        Returns a tuple of lists of starting and ending time instances (number
        of 5 minute intervals after day-start time) for which all machines in the 
        system are inactive.
        :param lst: List of number of active machines in each system at time 
                    interval of 5 minutes 
        """
        start_arr = []
        end_arr = []
        for i in range(len(self.sys_list)):
            start = []
            end = []
            for j in range(len(lst[i])):
                if lst[i][j]==0:
                    if j==0:
                        start.append(j)
                        continue
                    if j==len(lst[i])-1:
                        end.append(j)
                        continue
                    if lst[i][j-1]!=0:
                        start.append(j)
                    if lst[i][j+1]!=0:
                        end.append(j)
            start_arr.append(start)
            end_arr.append(end)
        return start_arr, end_arr

    def create_output_data(self):
        """
        Returns output data
        """
        pass
    
    def create_output_excel_file(self, dump_path, df, data):
        filename = 'output_'+os.path.basename(self.filepath)
        workbook = xlsxwriter.Workbook(os.path.join(dump_path, filename))
        worksheet = workbook.add_worksheet(df[1][0])
        merge_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'
        })
        head_format = workbook.add_format({
            'bold':1,
            'border':1,
        })
        worksheet.set_column('A:A', 12)
        worksheet.set_column('I:I', 18)
        worksheet.merge_range('A1:B1', 'System Information', merge_format)
        worksheet.merge_range('C1:I1', 'Stoppage Information', merge_format)
        worksheet.write('A2', 'System Name', head_format)
        worksheet.write('B2', 'Machines', head_format)
        worksheet.write('C2', 'Stoppage', head_format)
        worksheet.write('D2', 'Start Time', head_format)
        worksheet.write('E2', 'Start Date', head_format)
        worksheet.write('F2', 'End Time', head_format)
        worksheet.write('G2', 'End Date', head_format)
        worksheet.write('H2', 'Duration', head_format)
        worksheet.write('I2', 'Stoppage Reason', head_format)

        for i in range(len(data)):
            for j in range(len(data[0])):
                worksheet.write(i+2, j, data[i][j])
        workbook.close() 

