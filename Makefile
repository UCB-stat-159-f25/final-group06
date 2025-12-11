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

all:
	@echo "Running all notebooks:"
	@for nb in $(NOTEBOOKS); do \
		echo "Executing $$nb."; \
		conda run -n glacier-env jupyter nbconvert \
			--to notebook --execute $$nb --inplace \
			--ExecutePreprocessor.kernel_name="glacier-env"; \
	done
