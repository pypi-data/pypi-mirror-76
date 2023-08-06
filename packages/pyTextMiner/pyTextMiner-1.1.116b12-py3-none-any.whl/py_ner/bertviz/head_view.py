"""Module for postprocessing and displaying transformer attentions.

"""

import json
from py_ner.bertviz.attention import get_attention

import os

def show(model, model_type, tokenizer, decoding_ner_sentence, sentence_a, sentence_b=None):

    if sentence_b:
        vis_html = """
          <span style="user-select:none">
            Layer: <select id="layer"></select>
            Attention: <select id="filter">
              <option value="all">All</option>
              <option value="aa">Sentence A -> Sentence A</option>
              <option value="ab">Sentence A -> Sentence B</option>
              <option value="ba">Sentence B -> Sentence A</option>
              <option value="bb">Sentence B -> Sentence B</option>
            </select>
          </span>
          <div id='vis'></div> 
        """
    else:
        vis_html = """
          <span style="user-select:none">
            Layer: <select id="layer"></select>
            Attention: <select id="filter">
              <option value="all">All</option>
              <option value="aa">Sentence A -> Sentence A</option>
            </select>
          </span>
          <div id='vis'></div> 
        """

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    vis_js = open(os.path.join(__location__, 'head_view.js')).read()
    attn_data = get_attention(model, model_type, tokenizer, sentence_a, sentence_b)
    params = {
        'attention': attn_data,
        'default_filter': "all"
    }

    with open('bert_visualization.html', 'w') as f:
        _head = "<html><meta charset=\"utf-8\"><head><title>BERT Attention Visualization</title>" \
                "<script src=\"https://requirejs.org/docs/release/2.3.6/minified/require.js\" type=\"text/javascript\"></script></head>\n<body>"

        _body = "<script>\n" \
                "require.config({\n" \
                    "paths: {\n" \
                                "\"d3\": \"https//cdnjs.cloudflare.com/ajax/libs/d3/3.4.8/d3.min\",\n" \
                                "\"jquery\": \"https//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min\"," \
                            "}\n" \
                        "});\n"

        f.write(_head)

        f.write('\n' + vis_html + '\n')
        f.write('\n' + "<h2>")
        f.write(decoding_ner_sentence)
        f.write('\n' + "</h2>\n")

        f.write(_body)

        f.write('window.params = %s' % json.dumps(params) + '\n')
        #f.write("\n</script>")
        #f.write("<script>")
        f.write(vis_js + '\n')
        f.write("\n</script>")

        f.write("</body></html>")
