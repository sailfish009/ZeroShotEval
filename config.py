"""Config file for ZeroShotEval launcher scripts

This module contains config settings for all modules in ZeroShotEval toolkit 
in the format of easydict dictionaries.


Already contains the following configs:

Neural networks:
    - CADA-VAE (incomplete)  \\TODO: Verify CADA-VAE configs
    - 

Datasets:
    - CUB (incomplete)  \\TODO: Verify CUB configs
"""

# TODO:
#     * Add AWA2, SUN datasets conf
#     * Add GAN conf
#     * Add embeddings conf
#     * etc.


from easydict import EasyDict as edict


#region GLOBAL DEFAULT CONFIGS
default = edict()

default.model = 'cada_vae'
default.datasets = 'cub,awa2'

default.modalities = 'img,cls_attr'
default.img_net = 'resnet101'
default.cls_attr_net = 'word2vec'

default.saved_obj_embeddings_path = ''  # path to stored object embeddings to load
default.obj_embeddings_save_path = ''  # path to save computed embeddings

default.compute_train_zsl_embeddings = True
#endregion


#region MODEL CONFIGS
model = edict()

model.general_parameters = edict()  # general hyper for all models
model.general_parameters.device = "cpu"
model.general_parameters.num_shots = 0
model.general_parameters.generalized = True
model.general_parameters.batch_size = 32
model.general_parameters.nepoch = 100
model.general_parameters.fp16_train_mode = False  # for GPUs with tensor cores


#region CADA_VAE CONFIGS
model.cada_vae = edict()
model.cada_vae.model_name = "cada_vae"
# model.CADA_VAE.class_name = "CADA_VAE"
model.cada_vae.cross_resonstuction = True
model.cada_vae.distance = "wasserstein"

model.cada_vae.specific_parameters = edict()
model.cada_vae.specific_parameters.lr_gen_model = 0.00015
model.cada_vae.specific_parameters.loss = 'l1'
model.cada_vae.specific_parameters.latent_size = 64

model.cada_vae.specific_parameters.lr_cls = 0.001  # NOTE: probably for classification task only
model.cada_vae.specific_parameters.cls_train_epochs = 100  # early stopping nepoch стоит изменить
model.cada_vae.specific_parameters.auxiliary_data_source = 'attributes'  # для общности следует переделать эту и связанные части


# NOTE: эти парамертры стоит извлекать из генераторов эмбедингов/кэшированных эмбедингов.
# Их нужно перенести в dataset или куда-то ещё. 
# 
# Стоит ли развести скрытые слои для декодера/энкодера?


model.cada_vae.specific_parameters.hidden_layers = edict()
model.cada_vae.specific_parameters.hidden_layers.cnn_features = (1560, 1660)
model.cada_vae.specific_parameters.hidden_layers.attributes = (1450, 665)
model.cada_vae.specific_parameters.hidden_layers.sentences = (1450, 665)
model.cada_vae.specific_parameters.input_features_from_cnn = 2048  # for ResNet101

model.cada_vae.specific_parameters.hidden_size_rule = edict()
model.cada_vae.specific_parameters.hidden_size_rule.resnet_features = (1560, 1660)
model.cada_vae.specific_parameters.hidden_size_rule.attributes = (1450, 665)
model.cada_vae.specific_parameters.hidden_size_rule.sentences = (1450, 665)

model.cada_vae.specific_parameters.warmup = edict()
model.cada_vae.specific_parameters.warmup.beta = edict()
model.cada_vae.specific_parameters.warmup.beta.factor = 0.25
model.cada_vae.specific_parameters.warmup.beta.end_epoch = 93
model.cada_vae.specific_parameters.warmup.beta.start_epoch = 0

model.cada_vae.specific_parameters.warmup.cross_reconstruction = edict()
model.cada_vae.specific_parameters.warmup.cross_reconstruction.factor = 2.37
model.cada_vae.specific_parameters.warmup.cross_reconstruction.end_epoch = 75
model.cada_vae.specific_parameters.warmup.cross_reconstruction.start_epoch = 21

model.cada_vae.specific_parameters.warmup.distance = edict()
model.cada_vae.specific_parameters.warmup.distance.factor = 8.13
model.cada_vae.specific_parameters.warmup.distance.end_epoch = 22
model.cada_vae.specific_parameters.warmup.distance.start_epoch = 6

# NOTE: parameter below is for classification task only
model.cada_vae.specific_parameters.cls_train_steps = 29  # TODO: transfer auto selection from original repo
#endregion

#region CLSWGAN CONFIGS
model.clswgan = edict()
model.clswgan.model_name = 'clswgan'
# TODO: complete CLSWGAN CONFIGS section
#endregion

#endregion


#region DATASET CONFIGS
dataset = edict()

#region CUB DATASET CONFIGS
dataset.cub = edict()
dataset.cub.dataset_name = 'cub'
dataset.cub.path = "data/CUB_200_2011/"
dataset.cub.precomputed_embeddings_path = 'data/CUB/res101.mat'

dataset.cub.num_classes = 200
dataset.cub.num_novel_classes = 50
dataset.cub.samples_per_class = (200, 0, 400, 0) # ! Будет меняться от generalized (num_shots == 0). Данные значение для GZSL
# TODO: Стоит изменть для общности предыдущую строку

dataset.cub.class_embedding = edict()

dataset.cub.class_embedding.description_emb = edict()
dataset.cub.class_embedding.description_emb.module_name = ""
dataset.cub.class_embedding.description_emb.class_name = ""
dataset.cub.class_embedding.description_emb.have_pretrained = True
dataset.cub.class_embedding.description_emb.path = ""

dataset.cub.object_embedding = edict()

dataset.cub.object_embedding.resnet101 = edict()

dataset.cub.object_embedding.resnet101.module_name = ""
dataset.cub.object_embedding.resnet101.class_name = ""
dataset.cub.object_embedding.resnet101.have_pretrained = True
dataset.cub.object_embedding.resnet101.path = ""
#endregion

#region AWA2 DATASET CONFIGS
dataset.awa2 = edict()
dataset.awa2.dataset_name = "awa2"
# TODO: complete AWA2 DATASET CONFIGS section
#endregion 

#endregion


def generate_config(parsed_model, parsed_datasets):
    specific_model = model[parsed_model]
    for key, value in model.general_parameters.items():
        specific_model[key] = value

    datasets = {}
    for dataset_name in parsed_datasets:
        datasets[dataset_name] = dataset[dataset_name]

    return specific_model, datasets