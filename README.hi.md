# Kimi CLI

[![Commit Activity](https://img.shields.io/github/commit-activity/w/MoonshotAI/kimi-cli)](https://github.com/MoonshotAI/kimi-cli/graphs/commit-activity)
[![Checks](https://img.shields.io/github/check-runs/MoonshotAI/kimi-cli/main)](https://github.com/MoonshotAI/kimi-cli/actions)
[![Version](https://img.shields.io/pypi/v/kimi-cli)](https://pypi.org/project/kimi-cli/)
[![Downloads](https://img.shields.io/pypi/dw/kimi-cli)](https://pypistats.org/packages/kimi-cli)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/MoonshotAI/kimi-cli)

[中文](https://www.kimi.com/coding/docs/kimi-cli.html) | [English](./README.md)

Kimi CLI एक नया CLI एजेंट है जो आपके सॉफ्टवेयर विकास कार्यों और टर्मिनल संचालन में आपकी सहायता कर सकता है।

> [!IMPORTANT]
> Kimi CLI वर्तमान में तकनीकी पूर्वावलोकन में है।

## मुख्य विशेषताएं

- शेल जैसा UI और रॉ शेल कमांड निष्पादन
- Zsh एकीकरण
- [Agent Client Protocol] समर्थन
- MCP समर्थन
- और भी बहुत कुछ आने वाला है...

[Agent Client Protocol]: https://github.com/agentclientprotocol/agent-client-protocol

## इंस्टॉलेशन

> [!IMPORTANT]
> Kimi CLI वर्तमान में केवल macOS और Linux का समर्थन करता है। Windows समर्थन जल्द ही आ रहा है।

Kimi CLI को PyPI पर Python पैकेज के रूप में प्रकाशित किया गया है। हम इसे [uv](https://docs.astral.sh/uv/) के साथ इंस्टॉल करने की अत्यधिक अनुशंसा करते हैं। यदि आपने अभी तक uv इंस्टॉल नहीं किया है, तो कृपया इसे पहले इंस्टॉल करने के लिए [यहां](https://docs.astral.sh/uv/getting-started/installation/) दिए गए निर्देशों का पालन करें।

एक बार uv इंस्टॉल हो जाने के बाद, आप Kimi CLI को इस तरह इंस्टॉल कर सकते हैं:

```sh
uv tool install --python 3.13 kimi-cli
```

यह जांचने के लिए `kimi --help` चलाएं कि Kimi CLI सफलतापूर्वक इंस्टॉल हुआ है या नहीं।

> [!IMPORTANT]
> macOS पर सुरक्षा जांच के कारण, पहली बार जब आप `kimi` कमांड चलाते हैं तो आपके सिस्टम वातावरण के आधार पर 10 सेकंड या अधिक समय लग सकता है।

## अपग्रेड करना

Kimi CLI को नवीनतम संस्करण में अपग्रेड करने के लिए:

```sh
uv tool upgrade kimi-cli --no-cache
```

## उपयोग

उस डायरेक्टरी में `kimi` कमांड चलाएं जिस पर आप काम करना चाहते हैं, फिर Kimi CLI को सेटअप करने के लिए `/setup` भेजें:

![](./docs/images/setup.png)

सेटअप के बाद, Kimi CLI उपयोग के लिए तैयार हो जाएगा। अधिक जानकारी प्राप्त करने के लिए आप `/help` भेज सकते हैं।

## विशेषताएं

### शेल मोड

Kimi CLI केवल एक कोडिंग एजेंट नहीं है, बल्कि एक शेल भी है। आप `Ctrl-X` दबाकर मोड को स्विच कर सकते हैं। शेल मोड में, आप Kimi CLI को छोड़े बिना सीधे शेल कमांड चला सकते हैं।

> [!NOTE]
> `cd` जैसे बिल्ट-इन शेल कमांड अभी तक समर्थित नहीं हैं।

### Zsh एकीकरण

आप अपने शेल अनुभव को AI एजेंट क्षमताओं के साथ सशक्त बनाने के लिए Kimi CLI को Zsh के साथ उपयोग कर सकते हैं।

[zsh-kimi-cli](https://github.com/MoonshotAI/zsh-kimi-cli) प्लगइन को इस तरह इंस्टॉल करें:

```sh
git clone https://github.com/MoonshotAI/zsh-kimi-cli.git \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/kimi-cli
```

> [!NOTE]
> यदि आप Oh My Zsh के अलावा किसी अन्य प्लगइन मैनेजर का उपयोग कर रहे हैं, तो आपको इंस्टॉलेशन निर्देशों के लिए प्लगइन के README को देखना पड़ सकता है।

फिर अपनी `~/.zshrc` में Zsh प्लगइन सूची में `kimi-cli` जोड़ें:

```sh
plugins=(... kimi-cli)
```

Zsh को पुनः आरंभ करने के बाद, आप `Ctrl-X` दबाकर एजेंट मोड में स्विच कर सकते हैं।

### ACP समर्थन

Kimi CLI [Agent Client Protocol] का तुरंत समर्थन करता है। आप इसे किसी भी ACP-संगत संपादक या IDE के साथ उपयोग कर सकते हैं।

उदाहरण के लिए, Kimi CLI को [Zed](https://zed.dev/) के साथ उपयोग करने के लिए, अपनी `~/.config/zed/settings.json` में निम्नलिखित कॉन्फ़िगरेशन जोड़ें:

```json
{
  "agent_servers": {
    "Kimi CLI": {
      "command": "kimi",
      "args": ["--acp"],
      "env": {}
    }
  }
}
```

फिर आप Zed के एजेंट पैनल में Kimi CLI थ्रेड्स बना सकते हैं।

### MCP टूल्स का उपयोग करना

Kimi CLI अच्छी तरह से स्थापित MCP कॉन्फ़िग कन्वेंशन का समर्थन करता है। उदाहरण के लिए:

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY"
      }
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

निर्दिष्ट MCP सर्वरों से कनेक्ट करने के लिए `--mcp-config-file` विकल्प के साथ `kimi` चलाएं:

```sh
kimi --mcp-config-file /path/to/mcp.json
```

## विकास

Kimi CLI को विकसित करने के लिए, चलाएं:

```sh
git clone https://github.com/MoonshotAI/kimi-cli.git
cd kimi-cli

make prepare  # विकास वातावरण तैयार करें
```

फिर आप Kimi CLI पर काम करना शुरू कर सकते हैं।

परिवर्तन करने के बाद निम्नलिखित कमांड्स देखें:

```sh
uv run kimi  # Kimi CLI चलाएं

make format  # कोड फॉर्मेट करें
make check  # लिंटिंग और टाइप चेकिंग चलाएं
make test  # टेस्ट चलाएं
make help  # सभी make टारगेट दिखाएं
```

## योगदान

हम Kimi CLI में योगदान का स्वागत करते हैं! अधिक जानकारी के लिए कृपया [CONTRIBUTING.md](./CONTRIBUTING.md) देखें।
