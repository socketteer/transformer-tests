import gpt_util

mask = {'yes': 100,
        'no': 100}
logit_bias = gpt_util.logit_mask(mask)