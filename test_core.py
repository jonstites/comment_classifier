from comment_generator.core import Comment, CommentReader, NgramCounter, MultiNgramCounter, Tokenizer, MarkovModel
from collections import Counter
import json
import io

def get_test_content():
    content = {
        "body": "my test comment",
        "subreddit": "my_test_subreddit"
    }
    return content

def get_test_comment():
    content = get_test_content()
    return Comment(content)

def test_comment_from_string():
    test_comment = get_test_comment()
    content_string = json.dumps(test_comment.content)
    
    comment = Comment.from_string(content_string)

    for key, value in test_comment.content.items():
        assert value == comment.content[key]

def test_comment_get_body():
    comment = get_test_comment()
    text = get_test_content()["body"]

    body = comment.get_body()

    assert body == text

def test_comment_eq():
    same_comment = get_test_comment()

    comment = get_test_comment()

    assert comment == same_comment
    assert not (comment != same_comment)

def test_comment_eq_diff():
    diff_comment = get_test_comment()
    diff_comment.content["subreddit"] = "all"

    comment = get_test_comment()

    assert comment != diff_comment
    assert not (comment == diff_comment)
    
def test_comment_reader_from_file():
    test_comment = get_test_comment()
    content = test_comment.content
    content_string = json.dumps(content)

    handle = io.StringIO(content_string)    

    count = 0
    for comment in CommentReader.from_file(handle):
        assert comment.content == content
        count += 1

    assert count == 1

def test_tokenizer_text_tokens():
    text = "A test text"
    test_tokens = ["A", "test", "text"]

    tokens = Tokenizer(text).get_text_tokens()
    
    assert tokens == test_tokens

def test_tokenizer_padded_tokens():
    tokenizer = Tokenizer("A test text")
    pad_token = tokenizer.pad_token
    ngram_size = 3
    expected_tokens = [pad_token, pad_token, "A", "test", "text"]
    
    tokens = tokenizer.get_padded_tokens(ngram_size)

    assert tokens == expected_tokens

def test_tokenizer_padded_tokens_unigram():
    tokenizer = Tokenizer("A test text")
    ngram_size = 1
    expected_tokens = ["A", "test", "text"]

    tokens = tokenizer.get_padded_tokens(1)

    assert tokens == expected_tokens

def test_tokenizer_tokens():
    tokenizer = Tokenizer("A test text")
    pad_token = tokenizer.pad_token
    end_token = tokenizer.end_token
    ngram_size = 2
    expected_tokens = [pad_token, "A", "test", "text", end_token]

    tokens = tokenizer.get_tokens(ngram_size)

    assert tokens == expected_tokens

def test_ngram_counter_add():
    text = "A text ngram text"
    ngram = NgramCounter(2)
    tokenizer = Tokenizer("")
    pad_token = tokenizer.pad_token
    end_token = tokenizer.end_token
    expected_ngrams = Counter(
        [(pad_token, "A"),
         ("A", "text"),
         ("text", "ngram"),
         ("ngram", "text"),
         ("text", end_token)
         ])


    ngram.add(text)
    ngrams = ngram.counts

    assert ngrams == expected_ngrams

def test_ngram_counter_eq():
    text = "A test ngram"
    expected_ngram = NgramCounter(2)
    expected_ngram.add(text)
    
    ngram = NgramCounter(2)
    ngram.add(text)

    assert ngram == expected_ngram
    assert not (ngram != expected_ngram)

def test_ngram_counter_eq_diff():
    text = "A test ngram"
    expected_ngram = NgramCounter(2)
    expected_ngram.add("A test ngram differs")
    
    ngram = NgramCounter(2)
    ngram.add(text)

    assert ngram != expected_ngram
    assert not (ngram == expected_ngram)

def test_multi_ngram_counter_eq():
    text = "A test text"
    expected_counter = MultiNgramCounter(2)
    expected_counter.add(text)

    ngram_counter = MultiNgramCounter(2)
    ngram_counter.add(text)

    assert ngram_counter == expected_counter
    assert not (ngram_counter != expected_counter)

def test_multi_ngram_counter_eq_diff():
    text = "A test text"
    expected_counter = MultiNgramCounter(2)
    expected_counter.add("A test text differs")

    ngram_counter = MultiNgramCounter(2)
    ngram_counter.add(text)

    assert ngram_counter != expected_counter
    assert not (ngram_counter == expected_counter)
    
def test_multi_ngram_counter_add():
    text = "A test text"
    unigrams = NgramCounter(1)
    unigrams.add(text)
    bigrams = NgramCounter(2)
    bigrams.add(text)
    expected_ngrams = [unigrams.counts, bigrams.counts]

    ngram_collection = MultiNgramCounter(2)
    ngram_collection.add(text)
    ngrams = [ngram.counts for ngram in ngram_collection.ngram_counters]

    assert ngrams == expected_ngrams
    
def test_markov_model_init():
    size = 5

    model = MarkovModel(size)

    assert model.max_ngram_size == size

def test_markov_model_reset_size():
    model = MarkovModel(1)
    new_size = 3

    model.reset_ngram_size(new_size)

    assert model.max_ngram_size == new_size

def test_markov_model_reset_ngrams():
    size = 2
    model = MarkovModel(size)
    model.add("some data")
    counters =  MultiNgramCounter(size).ngram_counters
    expected_ngrams = [counter.counts for counter in counters]

    model.reset_ngrams()
    ngrams = [counter.counts for counter in model.ngram_counters.ngram_counters]
    
    assert ngrams == expected_ngrams

def test_markov_model_add_ngrams():
    assert False
