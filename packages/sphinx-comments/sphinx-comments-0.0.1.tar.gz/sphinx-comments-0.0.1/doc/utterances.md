# Utterance

## Activate `utteranc.es`

You can activate `utteranc.es` by adding the following to your `conf.py` file:

```python
comments_config = {
   "utterances": {
      "repo": "github-org/github-repo",
      "optional": "config",
   }
}
```

```{note}
You can pass optional extra configuration for utterances. See
[the utterances documentation for your options](https://utteranc.es/#theme).
```

Next, [follow the `utteranc.es` configuration instructions](https://utteranc.es/#configuration).

When you build your documentation, pages will now have a comment box at the bottom. If readers log in via GitHub they will be able to post comments that will then map onto issues in your GitHub repository.

```{raw} html
<script
   type="text/javascript"
   src="https://utteranc.es/client.js"
   async="async"
   repo="executablebooks/sphinx-comments"
   issue-term="pathname"
   theme="github-light"
   label="💬 comment"
   crossorigin="anonymous"
/>
```