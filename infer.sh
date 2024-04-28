CUDA_VISIBLE_DEVICES=0 python inference.py \
    --config_file config/tco_fox.yaml \
    -l 1 \
    -p "drinking a beer" \
    -p "with a city in the background"


# CUDA_VISIBLE_DEVICES=1 python inference.py \
#     --config_file config/tco_student.yaml \
#     -l 6 \
#     -n 3 \
#     -p "doing assignment on his computer"


# CUDA_VISIBLE_DEVICES=2 python inference.py \
#     --config_file config/tco_3d_cat.yaml \
#     -p "near the Statue of Liberty" \
#     -p "as a police officer" \
#     -p "running in desert" \
#     -p "eating an avocado"

# CUDA_VISIBLE_DEVICES=3 python inference.py \
#     --config_file config/tco_child.yaml \
#     -p "eating a burger" \
#     -p "wearing a blue hat" \
#     -p "running in desert" \
#     -p "eating an avocado"


# CUDA_VISIBLE_DEVICES=1 python inference.py \
#     --config_file config/tco_mink.yaml \
#     -l 0 \
#     -n 3 \
#     -p "" \
#     -p "jogging on the beach" \
#     -p "enjoying a coffee meetup with a friend in the heart of New York City" \
#     -p "settling into his cozy apartment to review a paper"
