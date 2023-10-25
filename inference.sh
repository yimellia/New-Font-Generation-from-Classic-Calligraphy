#export CUDA_VISIBLE_DEVICES=1
python3 inference.py ./cfgs/inference204.yaml \
--weight ./results/LTX204/checkpoints/LTX204_3/last.pdparams \
--content_font ./meta204/jys \
--img_path ./meta204/train/LTX \
--saving_root ./test/test_results_JYS