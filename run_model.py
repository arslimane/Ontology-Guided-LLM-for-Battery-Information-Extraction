import sys
from main_code import getResultsCoT

# Arguments from the shell: model_name, pdf_file, ontology_file, chunk_size, output_file, max_new_tokens
model_name = sys.argv[1]
pdf_file = sys.argv[2]
ontology_file = sys.argv[3]
chunk_size = int(sys.argv[4])
output_file = sys.argv[5]
max_new_tokens = int(sys.argv[6])

getResultsCoT(model_name, pdf_file, ontology_file, chunk_size, output_file, max_new_tokens)