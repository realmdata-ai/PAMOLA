"""NLTK resources: found where the downloader puts them, and not checked at import.

``python -m nltk.downloader wordnet`` writes ``corpora/wordnet.zip``. NLTK reads the corpus from
it, but ``nltk.data.find("corpora/wordnet")`` raises ``LookupError``, so the package reported the
corpus as missing although it was installed — on every ``import pamola_core``, on stderr, with no
way for the user to make the message go away.
"""

import os
import subprocess
import sys
import zipfile

import pytest

nltk = pytest.importorskip("nltk")

from pamola_core.utils.nlp.remote_resources import nltk_resource_present  # noqa: E402


@pytest.fixture
def nltk_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(nltk.data, "path", [str(tmp_path)])
    return tmp_path


def test_a_zipped_corpus_is_present(nltk_dir):
    (nltk_dir / "corpora").mkdir()
    with zipfile.ZipFile(nltk_dir / "corpora" / "wordnet.zip", "w") as archive:
        archive.writestr("wordnet/lexnames", "00\tadj.all\t3\n")

    assert nltk_resource_present(nltk, "corpora/wordnet")


def test_an_unpacked_corpus_is_present(nltk_dir):
    (nltk_dir / "corpora" / "wordnet").mkdir(parents=True)

    assert nltk_resource_present(nltk, "corpora/wordnet")


def test_an_absent_corpus_is_not_present(nltk_dir):
    assert not nltk_resource_present(nltk, "corpora/wordnet")


def test_importing_the_package_checks_no_nlp_resource(tmp_path):
    env = dict(os.environ, NLTK_DATA=str(tmp_path))
    env.pop("PAMOLA_ALLOW_REMOTE_DOWNLOADS", None)
    code = ("import pamola_core\n"
            "from pamola_core.utils.nlp.remote_resources import get_degraded_resources\n"
            "print(sorted(get_degraded_resources()))")
    run = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, timeout=300)

    assert run.returncode == 0, run.stderr
    assert "nltk:" not in run.stdout + run.stderr


def test_english_lemmatization_without_wordnet_falls_back_to_the_stemmer(nltk_dir, monkeypatch):
    from pamola_core.utils.nlp import tokenization

    monkeypatch.setattr(tokenization, "_LEMMATIZERS", {})
    monkeypatch.setattr(tokenization, "_LEMMATIZERS_READY", False)

    assert tokenization.lemmatize(["running", "cars"], language="en") == ["run", "car"]
