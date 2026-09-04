#!/usr/bin/env python3
"""
Exporta cada slide .slide de um carrossel HTML (skill carrossel-instagram) como PNG.

Uso:
    python3 exportar_png.py caminho/do/carrossel.html pasta_de_saida/

Requer: pip install playwright && playwright install chromium
"""
import sys
import os


def main():
    if len(sys.argv) < 3:
        print("Uso: python3 exportar_png.py <carrossel.html> <pasta_saida>")
        sys.exit(1)

    html_path = os.path.abspath(sys.argv[1])
    out_dir = sys.argv[2]

    if not os.path.isfile(html_path):
        print(f"Erro: arquivo nao encontrado: {html_path}")
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright nao esta instalado neste ambiente.")
        print("Instale com:")
        print("  pip install playwright")
        print("  playwright install chromium")
        print("")
        print("Alternativa sem instalar nada: abra o HTML no navegador e use")
        print("o painel 'Exportar carrossel (PNG)' no final da pagina.")
        sys.exit(1)

    TARGET_WIDTH = 1080
    MAX_SCALE = 5  # protege contra device_scale_factor absurdo se o slide for muito estreito

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Fase 1: mede o slide em escala normal (device_scale_factor=1)
        probe_ctx = browser.new_context(viewport={"width": 1000, "height": 1200})
        probe_page = probe_ctx.new_page()
        probe_page.goto(f"file://{html_path}")
        probe_page.wait_for_timeout(400)  # fontes/imagens

        probe_slides = probe_page.query_selector_all(".slide")
        if not probe_slides:
            print("Nenhum elemento com classe '.slide' foi encontrado no HTML.")
            print("Confira se o carrossel foi gerado seguindo a skill carrossel-instagram.")
            probe_ctx.close()
            browser.close()
            sys.exit(1)

        total_slides = len(probe_slides)
        box = probe_slides[0].bounding_box()
        if not box or box["width"] == 0:
            print("Nao foi possivel medir a largura do primeiro slide.")
            probe_ctx.close()
            browser.close()
            sys.exit(1)

        slide_width = box["width"]
        scale = min(TARGET_WIDTH / slide_width, MAX_SCALE)
        probe_ctx.close()

        print(f"Encontrados {total_slides} slides ({slide_width:.0f}px de largura nativa).")
        print(f"Renderizando em escala {scale:.2f}x (~{slide_width * scale:.0f}px de largura final)...")

        # Fase 2: reabre com device_scale_factor calculado -> screenshot nativamente em alta resolucao
        ctx = browser.new_context(
            viewport={"width": 1000, "height": 1200},
            device_scale_factor=scale,
        )
        page = ctx.new_page()
        page.goto(f"file://{html_path}")
        page.wait_for_timeout(400)

        slides = page.query_selector_all(".slide")
        for i, slide in enumerate(slides, start=1):
            out_path = os.path.join(out_dir, f"slide-{i:02d}.png")
            slide.screenshot(path=out_path)
            print(f"  slide {i:02d}: {out_path}")

        ctx.close()
        browser.close()

    print(f"\nPronto! {total_slides} PNGs salvos em: {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
