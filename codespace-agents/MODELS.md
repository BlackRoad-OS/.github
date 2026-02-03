# Open Source AI Models for BlackRoad

> **All models are 100% open source and commercially friendly**

---

## Model Selection Criteria

All models included meet these requirements:
- ✅ Open source with permissive licenses
- ✅ Approved for commercial use
- ✅ No usage restrictions
- ✅ Can run locally or via API
- ✅ Active development and community support

---

## Available Models

### Code Generation Models

#### 1. **Qwen2.5-Coder** ⭐ Recommended for Code
- **License**: Apache 2.0
- **Sizes**: 0.5B, 1.5B, 3B, 7B, 14B, 32B
- **Context**: Up to 128K tokens
- **Use Cases**: Code generation, completion, debugging
- **Commercial**: ✅ Fully approved
- **Why**: State-of-the-art coding performance, beats many proprietary models
- **Install**: `ollama pull qwen2.5-coder`

#### 2. **DeepSeek-Coder**
- **License**: MIT
- **Sizes**: 1.3B, 6.7B, 33B
- **Context**: Up to 16K tokens
- **Use Cases**: Code completion, infilling, instruction following
- **Commercial**: ✅ Fully approved
- **Why**: Excellent code completion, trained on 2T tokens
- **Install**: `ollama pull deepseek-coder`

#### 3. **CodeLlama**
- **License**: Meta Community (Commercial OK)
- **Sizes**: 7B, 13B, 34B, 70B
- **Context**: Up to 100K tokens
- **Use Cases**: Code generation, debugging, refactoring
- **Commercial**: ✅ Approved with conditions (review Meta license)
- **Why**: Meta-backed, widely used, excellent performance
- **Install**: `ollama pull codellama`

### General Purpose Models

#### 4. **Llama 3.2** ⭐ Recommended for General Tasks
- **License**: Meta Community (Commercial OK)
- **Sizes**: 1B, 3B
- **Context**: 128K tokens
- **Use Cases**: Text generation, chat, reasoning
- **Commercial**: ✅ Approved with conditions
- **Why**: Latest Llama, efficient, multilingual
- **Install**: `ollama pull llama3.2`

#### 5. **Mistral 7B**
- **License**: Apache 2.0
- **Size**: 7B
- **Context**: 32K tokens
- **Use Cases**: Instruction following, chat, reasoning
- **Commercial**: ✅ Fully approved
- **Why**: High quality, efficient, proven track record
- **Install**: `ollama pull mistral`

#### 6. **Phi-3**
- **License**: MIT
- **Sizes**: 3.8B (mini), 7B (small), 14B (medium)
- **Context**: 128K tokens
- **Use Cases**: Reasoning, math, coding, analysis
- **Commercial**: ✅ Fully approved
- **Why**: Excellent reasoning, Microsoft-backed
- **Install**: `ollama pull phi3`

#### 7. **Gemma 2**
- **License**: Gemma Terms (Commercial OK)
- **Sizes**: 2B, 9B, 27B
- **Context**: 8K tokens
- **Use Cases**: Text generation, chat, summarization
- **Commercial**: ✅ Approved (see Gemma terms)
- **Why**: Google-quality, efficient, well-optimized
- **Install**: `ollama pull gemma2`

### Specialized Models

#### 8. **Qwen2.5**
- **License**: Apache 2.0
- **Sizes**: 0.5B to 72B
- **Context**: 128K tokens
- **Use Cases**: Multilingual tasks, reasoning, math
- **Commercial**: ✅ Fully approved
- **Install**: `ollama pull qwen2.5`

#### 9. **Mixtral 8x7B**
- **License**: Apache 2.0
- **Size**: 47B (8 experts × 7B)
- **Context**: 32K tokens
- **Use Cases**: Complex reasoning, multi-task
- **Commercial**: ✅ Fully approved
- **Why**: Mixture of Experts, excellent performance
- **Install**: `ollama pull mixtral`

---

## Model Comparison

| Model | Size | License | Commercial | Best For | Context |
|-------|------|---------|------------|----------|---------|
| **Qwen2.5-Coder** | 7B | Apache 2.0 | ✅ | Code generation | 128K |
| **DeepSeek-Coder** | 6.7B | MIT | ✅ | Code completion | 16K |
| **CodeLlama** | 7B-34B | Meta | ✅* | Code, refactoring | 100K |
| **Llama 3.2** | 1B-3B | Meta | ✅* | General chat | 128K |
| **Mistral** | 7B | Apache 2.0 | ✅ | Instructions | 32K |
| **Phi-3** | 3.8B | MIT | ✅ | Reasoning | 128K |
| **Gemma 2** | 2B-9B | Gemma | ✅* | Efficiency | 8K |

\* Review specific license terms for commercial use

---

## Recommended Agent Assignments

```yaml
coder_agent:
  primary: qwen2.5-coder:7b
  fallback: [deepseek-coder:6.7b, codellama:13b]

designer_agent:
  primary: llama3.2:3b
  fallback: [gemma2:9b, mistral:7b]

ops_agent:
  primary: mistral:7b
  fallback: [llama3.2:3b, phi3:mini]

analyst_agent:
  primary: phi3:medium
  fallback: [llama3.2:3b, mistral:7b]

docs_agent:
  primary: gemma2:9b
  fallback: [llama3.2:3b, mistral:7b]
```

---

## Local vs Cloud Strategy

### Local First (Ollama)
- Use for: Development, prototyping, cost savings
- Models: All listed above via Ollama
- Hardware: CPU or GPU, 8GB+ RAM recommended
- Cost: $0 per request

### Cloud Fallback
When local resources insufficient:
- **OpenAI**: GPT-4o-mini (~$0.15/1M tokens)
- **Anthropic**: Claude 3.5 Haiku (~$0.80/1M tokens)
- **Replicate**: Various models pay-per-use

---

## Installation

### Quick Install All Models
```bash
#!/bin/bash
# Install all BlackRoad agent models

echo "Installing code models..."
ollama pull qwen2.5-coder:7b
ollama pull deepseek-coder:6.7b
ollama pull codellama:13b

echo "Installing general models..."
ollama pull llama3.2:3b
ollama pull mistral:7b
ollama pull phi3:medium
ollama pull gemma2:9b

echo "✅ All models installed!"
ollama list
```

### Individual Install
```bash
# For coder agent
ollama pull qwen2.5-coder:7b

# For designer agent
ollama pull llama3.2:3b

# For ops agent
ollama pull mistral:7b

# For analyst agent
ollama pull phi3:medium

# For docs agent
ollama pull gemma2:9b
```

---

## Model Sizes & Requirements

| Model | Disk Space | RAM Required | Speed |
|-------|------------|--------------|-------|
| Qwen2.5-Coder 7B | 4.7 GB | 8 GB | Fast |
| DeepSeek-Coder 6.7B | 3.8 GB | 8 GB | Fast |
| CodeLlama 13B | 7.3 GB | 16 GB | Medium |
| Llama 3.2 3B | 2.0 GB | 4 GB | Very Fast |
| Mistral 7B | 4.1 GB | 8 GB | Fast |
| Phi-3 Medium | 7.9 GB | 16 GB | Medium |
| Gemma 2 9B | 5.4 GB | 12 GB | Fast |

**Total for all**: ~35 GB disk, recommend 32GB RAM for running multiple simultaneously

---

## License Summary

### Fully Permissive (No Restrictions)
- ✅ **Apache 2.0**: Qwen2.5, Mistral, Mixtral
- ✅ **MIT**: DeepSeek-Coder, Phi-3

### Permissive with Terms (Commercial OK)
- ✅ **Meta Community License**: Llama 3.2, CodeLlama
  - Free for commercial use under 700M MAUs
  - Most companies qualify
  
- ✅ **Gemma Terms**: Gemma 2
  - Free for commercial use
  - Attribution required
  - Review terms at ai.google.dev/gemma/terms

---

## Performance Benchmarks

### Code Generation (HumanEval)
- Qwen2.5-Coder 7B: **88.9%** ⭐
- DeepSeek-Coder 6.7B: 78.6%
- CodeLlama 13B: 35.1%

### General Tasks (MMLU)
- Phi-3 Medium: 78.0% ⭐
- Llama 3.2 3B: 63.0%
- Gemma 2 9B: 71.3%

### Reasoning (GSM8K Math)
- Phi-3 Medium: 91.0% ⭐
- Qwen2.5-Coder 7B: 83.5%
- Mistral 7B: 52.2%

---

## Cloud Provider Options

If you need cloud-hosted versions:

### Replicate
- All models available via API
- Pay per request
- No setup required
- Example: `replicate.com/meta/llama-3.2`

### Hugging Face Inference
- Free tier available
- Most models supported
- Easy integration

### Together.ai
- Optimized inference
- Competitive pricing
- Good for production

---

## Integration Example

```python
import ollama

# Local inference
response = ollama.chat(
    model='qwen2.5-coder:7b',
    messages=[{
        'role': 'user',
        'content': 'Write a Python function to calculate fibonacci'
    }]
)

print(response['message']['content'])
```

---

## Updates & Maintenance

Models are constantly improving. Update regularly:

```bash
# Update all models
ollama pull qwen2.5-coder:7b
ollama pull llama3.2:3b
# ... etc

# Check for updates
ollama list
```

---

## Additional Resources

- **Ollama**: https://ollama.ai
- **Qwen**: https://github.com/QwenLM/Qwen2.5-Coder
- **DeepSeek**: https://github.com/deepseek-ai/DeepSeek-Coder
- **Llama**: https://llama.meta.com
- **Mistral**: https://mistral.ai
- **Phi**: https://huggingface.co/microsoft/Phi-3-medium-4k-instruct
- **Gemma**: https://ai.google.dev/gemma

---

*100% open source. 0% vendor lock-in.*
