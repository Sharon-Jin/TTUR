lr_d=0.00006
lr_g=0.00004
update_k=True
k_constant=0.08
dataset=celebA_cropped
#dataset=lsun_cropped
train_stats_file="stats/stat_celebA_batched.pkl.gz"
lambda_k=0.001
gamma=0.5
python3 main_fid.py \
--dataset $dataset \
--train_stats_file $train_stats_file \
--input_height 64 \
--output_height 64 \
--is_crop False \
--is_train True \
--batch_size 16 \
--log_dir "logs" \
--d_lr $lr_d \
--g_lr $lr_g \
--lr_update_step 100000 \
--lambda_k $lambda_k \
--update_k $update_k \
--k_constant $k_constant \
--gamma $gamma \
--max_step 500000 \
--load_checkpoint False \
--checkpoint_name "" \
--start_step 0
