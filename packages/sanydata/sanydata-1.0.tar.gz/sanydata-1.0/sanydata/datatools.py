#!/usr/bin/env python
#coding=utf-8

import grpc
import data_message_pb2
import data_message_pb2_grpc


def get_files_list(stub, regex ='@@TYSFCB/@@2020-07@@fault@@.csv'):
    dainput = data_message_pb2.GetFileListInput(regex=regex)
    res = stub.GetFileList(dainput, timeout=20000)
    return res


def get_data(stub, file_list, columns=None):
    df_all = list()
    import zipfile
    import pandas as pd
    import io
    from io import StringIO
    import json
    dainput = data_message_pb2.GetTargetFileInput(filelist=json.dumps(file_list))
    if file_list[0].split('.')[-1] == 'gz':
        for i in stub.GetTargetFile(dainput, timeout=20000):
            try:
                f = zipfile.ZipFile(file=io.BytesIO(i.output))
                file_name = f.namelist()[0]
                turbine_num = file_name.split('#')[0]
                pure_data = f.read(file_name)
                fio = io.BytesIO(pure_data)
                with open('./gzfile_grpc_temp.csv.gz', "wb") as outfile:
                    outfile.write(fio.getbuffer())
                df = pd.read_csv('./gzfile_grpc_temp.csv.gz', compression='gzip')
                df['turbine_num'] = turbine_num
                os.remove('./gzfile_grpc_temp.csv.gz')
                df_all.append(df)
            except Exception as e:
                print(e)
    else: 
        for i in stub.GetTargetFile(dainput, timeout=20000):
            try:
                f = zipfile.ZipFile(file=io.BytesIO(i.output))
                file_name = f.namelist()[0]
                turbine_num = file_name.split('_')[1]
                pure_data = f.read(file_name)
                df = pd.read_csv(StringIO(pure_data.decode('utf-8')))
                df['turbine_num'] = turbine_num
                if columns:
                    df_all.append(df[columns + ['turbine_num']])
                else:
                    df_all.append(df)
            except Exception as e:
                print(e)
    if len(df_all) > 0:
        df_all = pd.concat(df_all)
        df_all = df_all.reset_index(drop=True)
    df_all = df_all.drop_duplicates()
    return df_all


def return_result(stub, project_name, data_start_time, data_end_time,
                  result=None, turbine_num=None, turbine_type=None, resultjson=None,
                  upload_fig_path=None, upload_log_path=None, upload_file_path=None, 
                  local_fig_path=None, local_log_path=None, local_file_path=None):
    import datetime
    import os
    mode_end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mode_start_time = os.getenv('ModelStartTime')
    wind_farm = os.getenv('WindFarm')
    task_id = os.getenv('TaskId')
    project_version = os.getenv('ProjectVersion')
    fig_fio = None
    log_fio = None
    file_fio = None
    # 本地图片处理
    if local_fig_path:
        with open(local_fig_path, 'rb') as f:
            fig_fio = f.read()
        os.remove(local_fig_path)
    # 本地日志处理
    if local_log_path:
        with open(local_log_path, 'rb') as f:
            log_fio = f.read()
        os.remove(local_log_path)
    # 本地其他文件处理
    if local_file_path:
        with open(local_file_path, 'rb') as f:
            file_fio = f.read()
        os.remove(local_file_path)
    
    data_input = data_message_pb2.ReturnResultInput(projectname=project_name, windfarm=wind_farm, turbine=turbine_num,
                                                    DataStartTime=data_start_time, DataEndTime=data_end_time,
                                                    ModeStartTime=mode_start_time, ModeEndTime=mode_end_time,
                                                    result=result, turbinetype=turbine_type, resultjson=resultjson,
                                                    uploadfigpath=upload_fig_path, fig=fig_fio, 
                                                    uploadlogpath=upload_log_path, log=log_fio, 
                                                    uploadfilepath=upload_file_path, file=file_fio)
    res = stub.ReturnResult(data_input, timeout=20000)
    return json.loads(res.code)
