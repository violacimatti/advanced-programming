from flask import Flask, render_template, request
from dataset import *
import operations
from decorator import *

app = Flask(__name__)

def get_df():
	d = GFF3Dataset('dataset.gff3')
	return d.dataframe

df1 = get_df()

av_operations = {
    'get_basic_info': 'Info: some basic information about the dataset',
    'get_unique_seqids': 'Sequence ID: list of unique sequence IDs available in the dataset',
    'get_unique_operations': 'Type operation: list of unique type of operations available in the dataset',
    'count_features_by_source': 'Count features: number of features provided by the same source',
    'count_entries_by_type': 'Count entries: number of entries for each type of operation',
    'entire_chromosome': 'Get entire chromosomes: new dataset containing only the information about entire chromosomes coming from source GRCh38',
    'fraction_unassembled': 'Count supercontigs: fraction of unassembled sequences from source GRCh38',
    'get_selected_sources': 'Entries from sources ensembl, havana, and ensembl_havana',
    'count_selected_operations': 'Count entries from ensembl, havana, and ensembl_havana: number of entries for each type of operation for the dataset containing containing only entries from source ensembl, havana and ensembl_havana',
    'get_gene_names': 'Gene names: gene names from the dataset containing containing only entries from source ensembl, havana and ensembl_havana'
    }
active_operations= {}
active_operations_descr= {}
for operation_name in av_operations:
     #take the functions from operations.py
     active_operations[operation_name]= getattr(operations, operation_name)
     active_operations_descr[operation_name]= av_operations.get(operation_name, 'Description missing')
     #active_operations[operation_name]= operations.decorator(getattr(operations, operation_name))
# Homepage
@app.route("/")
def homepage():
    return render_template("homepage.html")

# Active operations view
@app.route("/active_operations")
def active_operations_view():
    return render_template("active_operations.html", active_operations=active_operations, operation_descr=active_operations_descr)

# Execute operation and display result
@app.route("/execute_operation", methods=['POST'])
def execute_operation():
    operation_selected= request.form['select_operation']
    if operation_selected in active_operations:
         operation_result = active_operations[operation_selected](df1)
         return render_template("operation_result.html", operation_name=active_operations_descr[operation_selected], operation_result=operation_result)
    else:
         return 'The operation is not active'

# Project document view
@app.route("/project_document")
def project_document():
    return render_template("project_document.html")

if __name__ == "__main__":
    app.run(debug=True)