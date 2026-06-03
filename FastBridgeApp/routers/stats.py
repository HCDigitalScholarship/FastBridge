from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from stats_prompts import get_stats_summary, get_stats_compare_summary
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from pathlib import Path
from MongoDefinitionTools import get_title_location_levels, mg_get_locations, mg_get_sections, render_titles
from TextAnalyzer import TextAnalyzer

load_dotenv("FastBridgeApp/.env")


def _collect_analyzer_metrics(analyzer):
    """
    Helper function to collect all metrics from a TextAnalyzer instance.

    Returns: dict with all computed metrics
    """
    metrics = {}

    # Basic metrics
    metrics['textname'] = analyzer.get_textname()
    metrics['word_count'] = analyzer.num_words()
    metrics['vocab_size'] = analyzer.vocab_size()
    metrics['hapax'], metrics['hapax_percentage'] = analyzer.hapax_legonema()

    # Lexical metrics
    metrics['lex_dens'] = analyzer.lex_density()
    metrics['lex_sophistication'] = analyzer.lex_sophistication()
    metrics['lex_variation'] = analyzer.lex_variation()
    metrics['lex_r'] = analyzer.LexR()
    metrics['total_words_no_p'] = analyzer.totalWordsNoProper()
    metrics['unique_words_no_p'] = analyzer.uniqueWordsNoProper()
    metrics['avgWordLength'] = analyzer.avgWordLength()
    metrics['top20NoDie300'] = analyzer.top20NoDie300()

    # Frequency bins
    (metrics['freqBin1'], metrics['freqBin2'], metrics['freqBin3'],
     metrics['freqBin4'], metrics['freqBin5'], metrics['freqBin6']) = analyzer.freqBinMetrics()

    # Readability scores
    metrics['spache_score'] = analyzer.spache_score()
    metrics['dale_chall'], metrics['new_dale_chall'] = analyzer.dale_chall_score()
    metrics['ari'] = analyzer.ari_score()
    metrics['coleman_liau'] = analyzer.coleman_liau_score()
    metrics['lix_score'] = analyzer.lix_score()
    metrics['rix_score'] = analyzer.rix_score()
    metrics['smog_score'] = analyzer.smog_score()

    return metrics


def _build_context_dict(metrics, starts, ends, multiple_texts, plot_paths):
    """
    Helper function to build context dictionary for template rendering.

    Args:
        metrics: dict returned from _collect_analyzer_metrics
        starts: start section(s) as string
        ends: end section(s) as string
        multiple_texts: boolean indicating if multiple texts are being analyzed
        plot_paths: dict with keys 'freq_plot', 'cum_lex_plot', 'lin_lex_plot', 'freq_bins_plot'

    Returns: dict for template context
    """
    context = {
        "text_name": metrics['textname'] if not multiple_texts else metrics['textname'].split(" + "),
        "start_section": starts if not multiple_texts else starts.split("+"),
        "end_section": ends if not multiple_texts else ends.split("+"),
        "word_count": metrics['word_count'],
        "vocab_size": metrics['vocab_size'],
        "hapax_legomena": metrics['hapax'],
        "hapax_percentage": metrics['hapax_percentage'],
        "lexical_density": metrics['lex_dens'],
        "lexical_sophistication": metrics['lex_sophistication'],
        "lexical_variation": metrics['lex_variation'],
        "LexR": metrics['lex_r'],
        "smog": metrics['smog_score'],
        "total_words_no_proper": metrics['total_words_no_p'],
        "unique_words_no_proper": metrics['unique_words_no_p'],
        "avg_word_length": metrics['avgWordLength'],
        "top20_NoDie300": metrics['top20NoDie300'],
        "freq1": metrics['freqBin1'],
        "freq2": metrics['freqBin2'],
        "freq3": metrics['freqBin3'],
        "freq4": metrics['freqBin4'],
        "freq5": metrics['freqBin5'],
        "freq6": metrics['freqBin6'],
        "spache": metrics['spache_score'],
        "new_dale_chall": metrics['new_dale_chall'],
        "dale_chall": metrics['dale_chall'],
        "ari": metrics['ari'],
        "coleman_liau": metrics['coleman_liau'],
        "lix": metrics['lix_score'],
        "rix": metrics['rix_score'],
        "freq_plot_path": plot_paths['freq_plot'],
        "cum_lex_plot_path": plot_paths['cum_lex_plot'],
        "lin_lex_plot_path": plot_paths['lin_lex_plot'],
        "freq_bins_plot_path": plot_paths['freq_bins_plot'],
    }

    return context


def stats_compare_result(request, context, sourcetexts, starts, ends, language):
    analyzer_texts = sourcetexts.split('+')
    analyzer_starts = starts.split('+')
    analyzer_ends = ends.split('+')

    # Add text info to analyzer
    analyzers = []
    for i in range(len(analyzer_texts)):
        analyzer = TextAnalyzer()
        analyzer.add_text(analyzer_texts[i], language, analyzer_starts[i], analyzer_ends[i])
        analyzers.append(analyzer)

    # Getting Metrics, Hapax
    text_names = [a.texts[0][0].name for a in analyzers]
    text_starts = [a.texts[0][1] for a in analyzers]
    text_ends = [a.texts[0][2] for a in analyzers]

    texts_and_sections = mg_get_sections(language)

    # Clean up analyzer resources
    for analyzer in analyzers:
        del analyzer

    # add analyzer stats from each text to context
    context.update({
        "request": request,
        "textNames": text_names,
        "textStarts": text_starts,
        "textEnds": text_ends,
        "texts_and_sections": texts_and_sections,
    })

    return templates.TemplateResponse("stats-multiple-texts.html", context)

# Routing
router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")
from utils.assets import static_v
templates.env.globals["static_v"] = static_v
"""Expected Prefix: /stats"""

@router.get("/")
def stats_index(request: Request):
    return templates.TemplateResponse("stats-list-index.html", {"request": request})

@router.get("/mode-select/")
def stats_mode_selector(request: Request):
    return templates.TemplateResponse("stats-mode-selector.html", {"request": request})

@router.get("/{language}/{mode}/")
def stats_select(request: Request, language: str, mode: str):
    try:
        with open(f"data/Static/{language}_titles.json", "r", encoding="utf-8") as f:
            cache = json.load(f)
        titles = cache.get("titles", "")
    except Exception as e:
        print("Error loading titles:", e)
        title_location_levels = get_title_location_levels(language, depth=False)
        titles = render_titles(title_location_levels)
    
    return templates.TemplateResponse("stats_select.html", {"request": request,
                                                            "mode": mode,
                                                            "titles": titles})


@router.get("/select/sections/{textname}/{language}/")
def stats_select_section(textname: str, language: str):
    try:
        sectionDict = mg_get_sections(language, textname)
    except Exception:
        sectionDict = mg_get_locations(language, textname, get_index=False)

    return sectionDict


@router.post("/{language}/{mode}/result/{sourcetexts}/{starts}-{ends}/{running_list}/")
@router.get("/{language}/{mode}/result/{sourcetexts}/{starts}-{ends}/{running_list}/")
def stats_simple_result(request: Request, starts: str, ends: str, sourcetexts: str, language: str, running_list: str, mode: str):
    context = {}
    running_list = running_list == "running"

    if mode == 'Compare':
        return stats_compare_result(request, context, sourcetexts, starts, ends, language)

    # Create and populate analyzer
    analyzer = TextAnalyzer()
    multiple_texts = '+' in sourcetexts

    if multiple_texts:
        analyzer_texts = sourcetexts.split('+')
        analyzer_starts = starts.split('+')
        analyzer_ends = ends.split('+')

        for i in range(len(analyzer_texts)):
            analyzer.add_text(analyzer_texts[i], language, analyzer_starts[i], analyzer_ends[i])
    else:
        analyzer.add_text(sourcetexts, language, starts, ends)

    # Collect metrics using helper function
    metrics = _collect_analyzer_metrics(analyzer)

    # Generate plots
    plot_paths = {
        'freq_plot': analyzer.plot_word_freq(),
        'cum_lex_plot': analyzer.plot_cum_lex_load(),
        'lin_lex_plot': analyzer.plot_lin_lex_load(),
        'freq_bins_plot': analyzer.plot_freq_bin(),
    }

    # Clean up analyzer resources
    del analyzer

    # Build context using helper function
    context = _build_context_dict(metrics, starts, ends, multiple_texts, plot_paths)

    return templates.TemplateResponse("stats-single-text.html", {"context": context, "request": request})
   
@router.get("/get_metrics/{text_name}/{section_start}-{section_end}/{selected_index}")
def get_metrics_html(request: Request, text_name: str, section_start: str, section_end: str, selected_index: int):
    analyzer = TextAnalyzer()

    analyzer.add_text(text_name, "Latin", section_start, section_end)

    # Collect metrics using helper function
    metrics = _collect_analyzer_metrics(analyzer)

    # Calculate plot path numbers for multiple text comparison
    plotpath_nums = [0, 1, 2, 3]
    if selected_index > 0:
        plotpath_nums = [num + (4 * selected_index) for num in plotpath_nums]

    # Generate plots with custom indices
    plot_paths = {
        'freq_plot': analyzer.plot_word_freq(plotpath_nums[0]),
        'cum_lex_plot': analyzer.plot_cum_lex_load(plotpath_nums[1]),
        'lin_lex_plot': analyzer.plot_lin_lex_load(plotpath_nums[2]),
        'freq_bins_plot': analyzer.plot_freq_bin(plotpath_nums[3]),
    }

    # Clean up analyzer
    del analyzer

    # Build context using helper function (single text mode)
    context = _build_context_dict(metrics, section_start, section_end, False, plot_paths)

    # Timestamp for cache busting plots
    now = datetime.now()

    return templates.TemplateResponse('stats-column-data.html', {"context": context, "request": request, "now": now})


@router.get("/formulas")
def read_formulas(request: Request):
    return templates.TemplateResponse("stats-formulas.html", {"request": request})


class ChatRequest(BaseModel):
    message: str
    chat_id: str | None = None
    context: dict | None = None
    all_contexts: dict | None = None  # All loaded text contexts
    history: list[dict] = []
    initial: bool = False
    mode: str = "single"  # "single" or "compare"


@router.post("/chat")
def chat(req: ChatRequest):
    # Import genai only when chat endpoint is used (lazy import)
    import google.generativeai as genai

    api_key = os.getenv("API_KEY")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")
    
    if req.history:
        formatted_history = []
        for msg in req.history:
            if 'role' in msg and 'parts' in msg:
                # Convert role names to match Google AI expectations
                role = 'user' if msg['role'] == 'user' else 'model'
                formatted_history.append({
                    'role': role,
                    'parts': [{'text': msg['parts']}]
                })
        chat = model.start_chat(history=formatted_history)
    else:
        chat = model.start_chat()
    
    if req.initial:
        if req.mode == "compare":
            prompt_func = get_stats_compare_summary
        else:
            prompt_func = get_stats_summary
        
        # For compare mode, include all contexts in the prompt
        if req.mode == "compare" and req.all_contexts:
            all_contexts_str = json.dumps(req.all_contexts) if isinstance(req.all_contexts, dict) else str(req.all_contexts)
            system_prompt = prompt_func(context=all_contexts_str)
        else:
            context_str = json.dumps(req.context) if isinstance(req.context, dict) else req.context
            system_prompt = prompt_func(context=context_str)
        if req.mode == "compare":
            response = chat.send_message(system_prompt + "\n\nUser: " + req.message)
        else:
            response = chat.send_message(system_prompt)
    else:
        # Always include all loaded texts context in every message
        if req.all_contexts:
            for key, context in req.all_contexts.items():
                text_name = context.get('text_name', 'Unknown')
                hapax_count = len(context.get('hapax_legomena', [])) if context.get('hapax_legomena') else 'N/A'
                spache_score = context.get('spache', 'N/A')
                lex_r = context.get('LexR', 'N/A')
            
            # Include the FULL context data in the prompt
            full_context_str = json.dumps(req.all_contexts, indent=2)
            
            contexts_summary = "\n\n=== REMINDER: Currently Loaded Texts for Analysis ===\n"
            for key, context in req.all_contexts.items():
                text_name = context.get('text_name', 'Unknown')
                start_section = context.get('start_section', '')
                end_section = context.get('end_section', '')
                contexts_summary += f"✓ {text_name} ({start_section}-{end_section})\n"
                # Include key stats for each text
                word_count = context.get('word_count', 'N/A')
                vocab_size = context.get('vocab_size', 'N/A')
                lex_r = context.get('LexR', 'N/A')
                hapax_count = len(context.get('hapax_legomena', [])) if context.get('hapax_legomena') else 'N/A'
                spache_score = context.get('spache', 'N/A')
                contexts_summary += f"  - Word count: {word_count}, Vocab size: {vocab_size}, LexR: {lex_r}, Hapax words: {hapax_count}, Spache: {spache_score}\n"
            contexts_summary += "=== You have statistical data for ALL these texts ===\n\n"
            contexts_summary += f"=== FULL CONTEXT DATA ===\n{full_context_str}\n=== END CONTEXT DATA ===\n\n"
            enhanced_message = f"{contexts_summary}User Message: {req.message}"
        else:
            enhanced_message = req.message
            
        response = chat.send_message(enhanced_message)

    return {
        "response": response.text,
        "chat_id": req.chat_id
    }
