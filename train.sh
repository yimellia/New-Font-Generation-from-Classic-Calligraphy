#export CUDA_VISIBLE_DEVICES=4
python3 train.py \
    LTX204_3 \
    cfgs/custom204.yaml \
    --resume results/LTX204/checkpoints/LTX204_3/last.pdparams
