import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

print('[INFO] story_rewriter.py loaded')

class Rewriter:
    def __init__(self):
        print('[INFO] Rewriter instance created')
        self.model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.model_instance = AutoModelForCausalLM.from_pretrained(
            self.model,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )
    
    def rewrite(self, content, prompt="You are a professional story writer known for your rich third-person narration style.Rewrite the following passage from a strong third-person narrative perspective. Enhance the flow, add vivid descriptions, and make the emotions and actions more immersive. Keep the events and character dialogue faithful to the original."):
        print(f'[INFO] Rewriter.rewrite called with content: {str(content)[:100]}...')
        prompt = f"""[INST]{prompt}
Text:
{content}
[/INST]"""
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
        print(f'[DEBUG] Rewriter.rewrite result: {str(result)[:100]}...')
        result = result.split("Text:")[1]
        return result
