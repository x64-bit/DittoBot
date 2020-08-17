import tensorflow as tf
import gpt_2_simple as gpt2
import os
import requests

model_name = "355M"
if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)

file_name = "name_here.txt"

sess = gpt2.start_tf_sess()

gpt2.finetune(sess, 
			file_name, 
			model_name=model_name, 
			steps=2000,
			run_name='run1',
			print_every=10,
			sample_every=100)

#tf.global_variables_initializer()
single_text = gpt2.generate(sess, 
			length=100,
			temperature=1.0,
			nsamples=10,
			batch_size=10,
            prefix="<|startoftext|>",
			truncate="<|endoftext|>",
			include_prefix=False,
			return_as_list=True)[0]
print(single_text)