import os, warnings, time, gc, datetime, glob, random, pickle
import pandas as pd
from utilsnew import *
from pathlib import Path
import multiprocessing as mp
from argparse import ArgumentParser


def add_args(return_="parser"):

    parser = ArgumentParser()
    arg = parser.add_argument
    # can add multiple arguments from bash script...
    arg("--volume", default="OARS", help="Targes vs OARs")
    arg("--site",default="ALL",help="Only export contours for patient with set primary site...",)
    arg("--dataset", default="radcure", help="Preprocessing dataset as...?")
    arg("--input", default="/cluster/projects/radiomics/EXTERNAL/Head-Neck-PET-CT/", help="Input path as...?")
    arg("--output", default="/cluster/projects/radiomics/EXTERNAL/MASTRO2/", help="Output path as...?")

    if return_ == "parser":
        return parser
    else:
        args = parser.parse_args()
        return args

args = add_args(return_="args")
inputPath = args.input
outputPath = args.output
dataset = args.dataset

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d_%H%M%S")
root = Path(f"/cluster/home/jmarsill/EXPORT_{date}")
root_bad = Path(f"/cluster/home/jmarsill/EXPORT_{date}/bad")

# root_data = Path(f"/cluster/home/jmarsill/EXPORT_{date}/data")
# root.mkdir(exist_ok=True, parents=True)
# root_bad.mkdir(exist_ok=True, parents=True)
# root_data.mkdir(exist_ok=True, parents=True)
def save_bad(patient, save_path):
    bad_patient_files = [patient]
    df = pd.DataFrame(bad_patient_files, columns=["Bad_IMGs"])
    df.to_csv(f"{str(save_path)}/{patient}.csv", index=False)
    print(f"{patient} has a buggy in its tummy")


def working():
    laptop = "C://Users/Sejin/Documents/SegmentHN/"  # FOR LAPTOP
    server = "/cluster/home/sejinkim/SegmentHN/"  # FOR H4H
    joeServer = "/cluster/home/jmarsill/ProcessHN/"
    wkdir = laptop if os.path.isdir(laptop) else server
    try:
        os.chdir(wkdir)
        return wkdir

    except:
        os.chdir(joeServer)
        return joeServer

wkdir = working()
print(f"Working on: {wkdir}")
print(f"Starting to process dataset {dataset}")
config, exceptions = getConfig(wkdir, dataset)
print(config)
print(exceptions)

def process(data, bad_path=root_bad, roi_only=False, extract=args.volume, inputPath="/cluster/projects/radiomics/EXTERNAL/Head-Neck-PET-CT/"):
    # folder should be a tuple, can check for that
    temp, bad = [], ""
    # print(folder)
    startTime = time.time()
    # inputFolder = data['CT']['FolderPath']
    # rtstructFile = data['RTSTRUCT']['FilePath']
    # if 'Head-Neck-PET-CT' not in folder[0]:
    #     inputPath += 'Head-Neck-PET-CT/'
    #
    # inputFolder = inputPath + folder[0]
    # rtstructFolder = inputPath + folder[1]
    # sub_dir = os.listdir(inputFolder)
    rois = [ "GTV", "LNECK", "RNECK", "BRAIN", "BSTEM", "SPCOR", "ESOPH", "LARYNX",
             "MAND", "POSTCRI", "LPAR", "RPAR", "LACOU", "RACOU", "LMEAR", "RMEAR",
             "LLAC", "RLAC", "MRETRO", "RPLEX", "LPLEX", "LLENS", "RLENS", "LEYE",
             "REYE", "LOPTIC", "ROPTIC", "LSMAN", "RSMAN", "CHIASM", "LIPS", "OCAV",
             "TRAC", "THYR",  "SKIN"]

    # og_rois = [ "GTV", "LNECK", "RNECK", "BRAIN", "BSTEM", "SPCOR", "ESOPH", "LARYNX",
    #         "MAND", "POSTCRI", "LPAR", "RPAR", "LACOU", "RACOU", "LLAC", "RLAC",
    #         "RRETRO", "LRETRO", "RPLEX", "LPLEX", "LLENS", "RLENS", "LEYE", "REYE",
    #         "LOPTIC", "ROPTIC", "LSMAN", "RSMAN", "CHIASM", "LIPS", "OCAV", "IPCM",
    #         "SPCM", "MPCM"]
    # Load in dicom folder path AND RTSTRUCT folder....

    dicom = Dicom(data[0], structurePath=data[1], dataset=dataset, roi_only=roi_only, rois=rois, resample=False)
    fold = data[1].split('/')[-4]
    fold = fold
    warnings.warn(f"Saving {fold} in {outputPath}")
    # comment out when exporting...
    if roi_only!=True:
        dicom.export(outputPath, fold, exclude=["masks_save"], mode="itk",
                    resample=False, slices=False, spacing=None)
    # except Exception as e:
    #     warnings.warn(f'Code failed because of {e}.')
    #     bad = inputFolder + ' PAIR WRONG ' + rtstructFolder
    temp = dicom.roi_select
    temp2 = dicom.roi_list
    # print(dicom.spacing, dicom.origin)
    gc.collect()
    endTime = time.time()
    total_time = startTime - endTime
    print("Total Processing Time:", total_time)
    return bad, data, temp, temp2

def load_obj(name):
    with open(name, "rb") as f:
        return pickle.load(f)

def main(outputPath, exception_dict):
    print(outputPath)
    os.makedirs(outputPath, exist_ok=True)
    args = add_args(return_="args")
    start = time.time()
    print("hi", gc.isenabled())
    # data = pd.read_csv('/cluster/projects/radiomics/EXTERNAL/Head-Neck-PET-CT/1-combined-sets.csv', index_col=0)
    data = load_obj('/cluster/home/jmarsill/Temp/pkls/mastro.pkl')

    done = glob.glob('/cluster/projects/radiomics/EXTERNAL/MASTRO2/*')
    fnames = [d.split('/')[-1] for d in done] #.partition('.')[0]
    dicom_folders = [(data[i]['CT']['FolderPath'], data[i]['RTSTRUCT']['FilePath']) for i in range(len(data)) if data[i]['RTSTRUCT']['FilePath'].split('/')[-4] not in fnames]
    print(f'Processing {len(dicom_folders)} more folders.')
    # rtstruct = [(d['RTSTRUCT']['FilePath'] for i, d in enumerate(data)]
    # dicoms = [d['CT']['FolderPath'] for d in data]
    # make dicom_folders a tuple of paths...
    # dicom_folders = [(ct,rtstruct[i]) for i, ct in enumerate(dicoms)]
    p = mp.Pool(processes = (mp.cpu_count() - 1))
    results = p.map(process, dicom_folders)
    print(results)
    # save logs
    info, info2, problem = Info(ending='MFOUND'), Info(ending='MORIG'), BadFiles()
    for bad, patient, names_sel, names_orig in results:
        print(bad, patient[1], names_sel)
        info.add_patient(patient[1], names_sel)
        info2.add_patient(patient[1], names_orig)
        problem.add_bad(bad)

    os.makedirs(outputPath, exist_ok=True)
    info.export('/cluster/home/jmarsill/')  # uh fix this lol
    info2.export('/cluster/home/jmarsill/')
    problem.export('/cluster/home/jmarsill/')
    print(f"Script ran for {round((time.time()-start), 2)} seconds")
    return

if __name__ == "__main__":
    main(outputPath, exceptions)  # on desktop
