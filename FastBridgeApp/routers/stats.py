from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import os
import json
from datetime import datetime
from pathlib import Path
from MongoDefinitionTools import mg_render_titles, mg_get_locations, mg_get_sections, title_renaming_dict
from TextAnalyzer import TextAnalyzer


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

    texts_and_sections = mg_get_sections("Latin")

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
"""Expected Prefix: /stats"""

@router.get("/")
async def stats_index(request: Request):
    return templates.TemplateResponse("stats-list-index.html", {"request": request})

@router.get("/mode-select/")
async def stats_mode_selector(request: Request):
    return templates.TemplateResponse("stats-mode-selector.html", {"request": request})

@router.get("/{language}/{mode}/")
async def stats_select(request: Request, language: str, mode: str):
    return templates.TemplateResponse("stats_select.html", {"request": request,
                                                            "mode": mode,
                                                            "titles": mg_render_titles(language)})


@router.get("/select/sections/{textname}/{language}/")
async def stats_select_section(request: Request, textname: str, language: str):
    
    try:
        sectionDict = mg_get_sections(language, textname)
    except Exception as e:
        sectionDict = mg_get_locations(language, textname, get_index=False)
        
    return sectionDict


@router.post("/{language}/{mode}/result/{sourcetexts}/{starts}-{ends}/{running_list}/")
@router.get("/{language}/{mode}/result/{sourcetexts}/{starts}-{ends}/{running_list}/")
async def stats_simple_result(request: Request, starts: str, ends: str, sourcetexts: str, language: str, running_list: str, mode: str):
    context = {"request": request}
    running_list = running_list == "running"

    if mode == 'Compare': return stats_compare_result(request, context, sourcetexts, starts, ends, language)
    
    analyzer = TextAnalyzer()

    # check for multiple texts
    multiple_texts = '+' in sourcetexts

    if multiple_texts:
        analyzer_texts = sourcetexts.split('+')
        analyzer_starts = starts.split('+')
        analyzer_ends = ends.split('+')

        for i in range(len(analyzer_texts)):
            analyzer.add_text(analyzer_texts[i], language, analyzer_starts[i], analyzer_ends[i])
    else:
        analyzer.add_text(sourcetexts, language, starts, ends)

    textname = analyzer.get_textname()
    word_count = analyzer.num_words()
    vocab_size = analyzer.vocab_size()
    hapax, hapax_percentage = analyzer.hapax_legonema()
    lex_dens = analyzer.lex_density()
    lex_sophistication = analyzer.lex_sophistication()
    lex_variation = analyzer.lex_variation()
    lex_r = analyzer.LexR()
    total_words_no_p = analyzer.totalWordsNoProper()
    unique_words_no_p = analyzer.uniqueWordsNoProper()
    avgWordLength = analyzer.avgWordLength()
    top20NoDie300 = analyzer.top20NoDie300()
    freqBin1, freqBin2, freqBin3, freqBin4, freqBin5, freqBin6 = analyzer.freqBinMetrics()
    spache_score = analyzer.spache_score()
    dale_chall, new_dale_chall = analyzer.dale_chall_score()
    ari = analyzer.ari_score()
    coleman_liau = analyzer.coleman_liau_score()
    lix_score = analyzer.lix_score()
    rix_score = analyzer.rix_score()
    smog_score = analyzer.smog_score()


    freq_plot_path = analyzer.plot_word_freq()
    cum_lex_plot_path = analyzer.plot_cum_lex_load()
    lin_lex_plot_path = analyzer.plot_lin_lex_load()
    freq_bins_plot_path = analyzer.plot_freq_bin()
    
    # check if server works using above. if not, uncomment/figure something out
    # base_path = '/FastBridge/FastBridgeApp/static/assets/plots/'
    # freq_relative_plot_path = os.path.relpath(freq_plot_path, start=base_path)
    # cum_lex_relative_plot_path = os.path.relpath(cum_lex_plot_path, start=base_path)
    # lin_lex_relative_plot_path = os.path.relpath(lin_lex_plot_path, start=base_path)
    # freq_bins_relative_plot_path = os.path.relpath(freq_bins_plot_path, start=base_path)

    context.update({
        "text_name": textname if not multiple_texts else textname.split(" + "),
        "start_section": starts if not multiple_texts else starts.split("+"),
        "end_section": ends if not multiple_texts else ends.split("+"),
        "word_count": word_count,
        "vocab_size": vocab_size,
        "hapax_legonema": hapax,
        "hapax_percentage": hapax_percentage,
        "lexical_density": lex_dens,
        "lexical_sophistication": lex_sophistication,
        "lexical_variation": lex_variation,
        "LexR": lex_r,
        "smog": smog_score,
        "total_words_no_proper": total_words_no_p,
        "unique_words_no_proper": unique_words_no_p,
        "avg_word_length": avgWordLength,
        "top20_NoDie300": top20NoDie300,
        "freq1": freqBin1,
        "freq2": freqBin2,
        "freq3": freqBin3,
        "freq4": freqBin4,
        "freq5": freqBin5,
        "freq6": freqBin6,
        "spache": spache_score,
        "new_dale_chall": new_dale_chall,
        "dale_chall": dale_chall,
        "ari": ari,
        "coleman_liau": coleman_liau,
        "lix": lix_score,
        "rix": rix_score,
        "freq_plot_path": freq_plot_path,
        "cum_lex_plot_path": cum_lex_plot_path,
        "lin_lex_plot_path": lin_lex_plot_path,
        "freq_bins_plot_path": freq_bins_plot_path,
        # "freq_plot_path": freq_relative_plot_path,
        # "cum_lex_plot_path": cum_lex_relative_plot_path,
        # "lin_lex_plot_path": lin_lex_relative_plot_path,
        # "freq_bins_plot_path": freq_bins_relative_plot_path
    })

    return templates.TemplateResponse("stats-single-text.html", context)
   
@router.get("/get_metrics/{text_name}/{section_start}-{section_end}/{selected_index}")
async def get_metrics_html(request: Request, text_name: str, section_start: str, section_end: str, selected_index: int):
    context = {"request": request}
    
    analyzer = TextAnalyzer()
    
    analyzer.add_text(text_name, "Latin", section_start, section_end)

    textname = analyzer.get_textname()
    word_count = analyzer.num_words()
    vocab_size = analyzer.vocab_size()
    hapax, hapax_percentage = analyzer.hapax_legonema()
    lex_dens = analyzer.lex_density()
    lex_sophistication = analyzer.lex_sophistication()
    lex_variation = analyzer.lex_variation()
    lex_r = analyzer.LexR()
    total_words_no_p = analyzer.totalWordsNoProper()
    unique_words_no_p = analyzer.uniqueWordsNoProper()
    avgWordLength = analyzer.avgWordLength()
    top20NoDie300 = analyzer.top20NoDie300()
    freqBin1, freqBin2, freqBin3, freqBin4, freqBin5, freqBin6 = analyzer.freqBinMetrics()
    spache_score = analyzer.spache_score()
    dale_chall, new_dale_chall = analyzer.dale_chall_score()
    ari = analyzer.ari_score()
    coleman_liau = analyzer.coleman_liau_score()
    lix_score = analyzer.lix_score()
    rix_score = analyzer.rix_score()
    smog_score = analyzer.smog_score()
    
    # Remove file path references and use database for plots (if applicable)
    plotpath_nums = [0, 1, 2, 3]
    if selected_index > 0:  # if the selected index isn't the first set of graphs
        plotpath_nums = [num + (4 * selected_index) for num in plotpath_nums]

    freq_plot_path = analyzer.plot_word_freq(plotpath_nums[0])
    cum_lex_plot_path = analyzer.plot_cum_lex_load(plotpath_nums[1])
    lin_lex_plot_path = analyzer.plot_lin_lex_load(plotpath_nums[2])
    freq_bins_plot_path = analyzer.plot_freq_bin(plotpath_nums[3])

    now = datetime.now()  # for caching issue with plots
    
    context.update({
        "request": request,
        "text_name": textname,
        "start_section": section_start,
        "end_section": section_end,
        "word_count": word_count,
        "vocab_size": vocab_size,
        "hapax_legomena": hapax,
        "hapax_percentage": hapax_percentage,
        "lexical_density": lex_dens,
        "lexical_sophistication": lex_sophistication,
        "lexical_variation": lex_variation,
        "LexR": lex_r,
        "smog": smog_score,
        "total_words_no_proper": total_words_no_p,
        "unique_words_no_proper": unique_words_no_p,
        "avg_word_length": avgWordLength,
        "top20_NoDie300": top20NoDie300,
        "freq1": freqBin1,
        "freq2": freqBin2,
        "freq3": freqBin3,
        "freq4": freqBin4,
        "freq5": freqBin5,
        "freq6": freqBin6,
        "spache": spache_score,
        "new_dale_chall": new_dale_chall,
        "dale_chall": dale_chall,
        "ari": ari,
        "coleman_liau": coleman_liau,
        "lix": lix_score,
        "rix": rix_score,
        "freq_plot_path": freq_plot_path,
        "cum_lex_plot_path": cum_lex_plot_path,
        "lin_lex_plot_path": lin_lex_plot_path,
        "freq_bins_plot_path": freq_bins_plot_path,
        "now": now
    })

    return templates.TemplateResponse('stats-column-data.html', context)


@router.get("/formulas")
async def read_formulas(request: Request):
    return templates.TemplateResponse("stats-formulas.html", {"request": request})


@router.get("/cumulative/{language}/")
async def stats_cumulative(request: Request, language: str):
    # Retrieve the selected text names from the session or storage
    # Replace with your storage retrieval logic
    selected_texts = retrieve_selected_texts()

    # Process the selected text names and retrieve the corresponding book data
    sectionDict = mg_get_sections(language)
    sectionBooks = [sectionDict[textname] for textname in selected_texts]

    # Perform cumulative statistics calculations or any other operations on sectionBooks

    return templates.TemplateResponse("stats_cumulative.html", {"request": request, "sectionBooks": sectionBooks})
