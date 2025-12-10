env:
	@echo "Creating or updating conda environment:"
	@if conda env list | grep -q glacier-env; then \
		echo "Environment exists, updating from environment.yml"; \
		conda env update -n glacier-env -f environment.yml; \
	else \
		echo "Creating from environment.yml"; \
		conda env create -n glacier-env -f environment.yml; \
	fi

NOTEBOOKS = eda.ipynb karakoram_analysis.ipynb non-karakoram_analysis.ipynb main.ipynb

all: env
	@echo "Running all notebooks:"
	@for nb in $(NOTEBOOKS); do \
		echo "Executing $$nb."; \
		conda run -n glacier-env jupyter nbconvert \
			--to notebook --execute $$nb --inplace \
			--ExecutePreprocessor.kernel_name="glacier-env"; \
	done

pdfs:
	@echo "Exporting notebooks to pdf_builds directory"
	@for nb in $(NOTEBOOKS); do \
		echo "Exporting $$nb to PDF"; \
		myst build $$nb --pdf; \
		PDF_NAME=$$(basename $$nb .ipynb | tr '_' '-').pdf; \
		mv _build/exports/$$PDF_NAME pdf_builds/; \
	done
	@echo "All notebooks exported to pdf_builds"
