import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class rewriter:
    def __init__(self):
        self.model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.model_instance = AutoModelForCausalLM.from_pretrained(
            self.model,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )
    
    def rewrite(self, story):
        prompt = f"[INST] Rewrite this story in a more engaging way: {story} [/INST]"
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model_instance.device)
        with torch.no_grad():
            output = self.model_instance.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.9,
                top_p=0.95,
                do_sample=True,
                repetition_penalty=1.1
            )
        result = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return result
