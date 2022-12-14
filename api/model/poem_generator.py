import torch
import torch.nn.functional as F
from tqdm import trange
from transformers import GPT2Tokenizer


class PoemGenerator:

    def __init__(self, model_path, tokenizer='DeepESP/gpt2-spanish', device="cpu"):
        if not torch.cuda.is_available():
            self.model = torch.load(model_path, map_location=torch.device('cpu')).to(device)
        else:
            self.model = torch.load(model_path).to(device)
        self.tokenizer = GPT2Tokenizer.from_pretrained(tokenizer)

    def generate(self, prompt, entry_count=5, entry_length=30, top_p=0.8, temperature=1., ):
        self.model.eval()
        generated_num = 0
        generated_list = []

        filter_value = -float("Inf")

        with torch.no_grad():

            for entry_idx in trange(entry_count):

                entry_finished = False
                generated = torch.tensor(self.tokenizer.encode(prompt)).unsqueeze(0)

                for i in range(entry_length):
                    outputs = self.model(generated, labels=generated)
                    loss, logits = outputs[:2]
                    logits = logits[:, -1, :] / (temperature if temperature > 0 else 1.0)

                    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                    cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

                    sorted_indices_to_remove = cumulative_probs > top_p
                    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                    sorted_indices_to_remove[..., 0] = 0

                    indices_to_remove = sorted_indices[sorted_indices_to_remove]
                    logits[:, indices_to_remove] = filter_value

                    next_token = torch.multinomial(F.softmax(logits, dim=-1), num_samples=1)
                    generated = torch.cat((generated, next_token), dim=1)

                    if next_token in self.tokenizer.encode("<|endoftext|>"):
                        entry_finished = True

                    if entry_finished:
                        generated_num = generated_num + 1

                        output_list = list(generated.squeeze().numpy())
                        output_text = self.tokenizer.decode(output_list)
                        generated_list.append(output_text)
                        break

                if not entry_finished:
                    output_list = list(generated.squeeze().numpy())
                    output_text = f"{self.tokenizer.decode(output_list)}<|endoftext|>"
                    generated_list.append(output_text)

        return generated_list


if __name__ == "__main__":
    generator = PoemGenerator("spanish_poems_model.pt")
    result = generator.generate("Una ma??ana cualquiera\nal otro lado del valle\ncorr??a una dulce brisa",entry_count=5)
    print()
    for poem in result:
        print(poem)
        print()
