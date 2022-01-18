from argparse import ArgumentParser

def add_args(return_="parser"):
    parser = ArgumentParser()
    arg = parser.add_argument

    # Lightning Specific GPU Args
    arg("--overfit", type=bool, default=False,
        help="Set TRUE to turn AUG off during training.")
    arg("--gpus", type=str, default='4', help="how many gpus")
    arg("--dir-path", type=str, default="/cluster/home/jmarsill",
        help='root location of SegmentHN folder')
    arg("--backend", type=str, default="dp",
        help="supports three options dp, ddp, ddp2")
    arg("--use-16bit", type=bool, default=False,
        help="if true uses 16 bit precision")

    # model specific parameters
    arg("--root", default="models/unet", help="checkpoint root")
    arg("--batch-size", type=int, default=16)
    arg("--lr", type=float, default=0.001)
    arg("--workers", type=int, default=6)
    arg("--clean", action="store_true")
    arg("--decay", type=float, default=0)
    arg("--gamma", type=float, default=0.99,
        help="Value for learning rate decay")
    arg("--deform", type=bool, default=False)
    arg("--project", type=bool, default=False)
    arg("--decay-after",type=int,default=4,
        help="Decay lr after X amount of epochs...",)
    arg("--n-classes", type=int, default=1)
    arg("--overfit-by", type=float, default=0.01)
    arg("--n-epochs", type=int, default=1000)
    arg("--clip-min", type=int, default=-200)
    arg("--clip-max", type=int, default=300)
    arg("--reload", type=bool, default=False)
    arg( "--feature-scale", type=int, default=4,
        help="Scale features in attention unet. If 4 will start with 16 feature maps.")
    arg("--window",type=int,default=5,
        help="Default 5, Crop slices input +/-5 slices with center as reference.")
    arg("--scale-factor",type=float, default=1.,
        help="Scales starting filter count in model. (orig 16 will be 32...)")
    arg("--crop-factor", type=int, default=512)
    arg("--lr-step", type=int, default=24000)
    arg( "--scale-weights", type=float, default=1.0,
        help="Standard taken as 512x512 per slice...",)
    arg("--f-maps", type=int, default=32,
        help="For 3D models, defines number of feature maps used.", )
    arg("--num-groups", type=int, default=8,
        help="NOTE: f_maps must be dividable by num_groups. 3D models.")
    arg("--crop-as", type=str, default="standard",
        help="If 3D will crop volume by 3D mask COM. Anything else uses thresholding 2D slice of image. ")
    arg("--filter", type=bool, default=False,
        help="Used to process new RESAMPLED RADCURE with masks located in /cluster/projects/radiomics/Temp/RESAMPLED")
    arg("--testing", type=bool, default=False)
    arg("--metrics-name", type=str, default="METRICSGNECK_2020_02_18_100330")
    arg("--spacing", type=str, default="1mm")
    arg("--volume-type", type=str, default="targets")
    arg("--oar-version", type=int, default=18)
    arg("--dce-version", type=int, default=1)

    # Load previous model
    arg("--load-from-mets", type=bool, default=False)
    arg( "--weights-path", type=str,
        default="/home/gpudual/bhklab/private/jmarsill/models/WOLNET_2020_05_14_205841/lightning_logs/version_0/checkpoints/'epoch=0.ckpt'")
    arg("--meta-path", type=str,
        default="/home/gpudual/bhklab/private/jmarsill/models/WOLNET_2020_05_14_205841/lightning_logs/version_0/checkpoints/meta_tags.csv")
    arg("--external",type=bool, default=False)
    arg("--resample", type=bool, default=False, help='Set to True if using PDDCA dataset...')
    # arg("--dataset", type=str, default='OAR', help='Set to OAR or GTV.')
    # Training specific parameters
    arg("--model", type=str, default="UNET")
    # arg("--test", type=bool, default=False)
    arg("--aug-prob", type=float, default=0.3)
    arg("--scheduler-type", type=str, default='step')
    arg("--scheduler", type=bool, default=True)
    arg("--sub-enc", type=bool, default=False)
    arg("--crop", type=bool, default=False)
    arg("--shuffle-data", type=bool, default=False)
    arg("--new-loss", type=bool, default=False)
    arg("--fold", type=int, help="fold", default=0)
    arg("--single-loss", type=str, default="both")  # all dices at once..
    arg("--model-path", type=str, default="/home/gpudual/bhklab/private/jmarsill/models")
    arg("--mask-path", type=str, default="/home/gpudual/bhklab/private/jmarsill/masks")
    arg("--img-path",type=str, default="/home/gpudual/bhklab/private/jmarsill/img")
    arg( "--device-ids", type=str, default="0,1,2,3",
        help="For example 0,1 to run on two GPUs" )
    arg("--size", type=str, default="512x512",
        help="Input size, for example 244x244 crop. Must be multiples of 32")
    # arg("--resample", type=int, default=2,
    #     help="For Data Augmentation of Dataset. default=3. Can resample same slice (1,2,3...N) or None times.")
    arg("--loss", type=str, default="DICE", help="Loss Name (DICE is default)")
    arg("--optim", type=str, default="SGD", help="Optimizer: ADAM v. SGD w/ Momentum")
    arg("--verbose", type=bool, default=True,
        help="if True, Print Various Model Outputs...")
    arg("--mode", type=str, default="train",
        help="Test to run with unit test...")
    arg("--model-name", type=str, default=None,
        help="To continue at previously saved model...")
    arg("--site", type=str, default="Oropharynx",
        help="Oropharynx, Larynx, or Nasopharynx ...")
    arg( "--pkl-name", type=str, default="RADGTV_full",
        help="Use databunch.py to create dictionary to iterate through...")
    arg("--data", type=str, default="RADCURE",
        help="RADCURE or OTHER, OTHER USES SEGMENTHN19 DATA")
    arg("--norm", type=str, default="standard",
        help="True to renormalize data by MIN:MAX window...")
    arg("--split-mode", type=str, default="default",
        help="External use default. Radcure use csv_full",)
    arg("--tt-split", type=float, default=1, help="Default = no train/test splitting")
    arg( "--mrn-csv-path", type=str,
        default="/home/gpudual/SegmentHN/data/valid_mrns_by_dssite_new2.csv",
        help="Main .csv patients divieded by HNC disease site.")

    if return_ == "parser":
        return parser
    else:
        args = parser.parse_args()
        return args
