import io;
import sys;
import files;
import string;
import python;
import R;

string emews_root = getenv("EMEWS_PROJECT_ROOT");
string turbine_output = getenv("TURBINE_OUTPUT");

string to_xml_code =
"""
import json2xml
import json
params = json.loads(r'''%s''')

default_settings = '%s'
xml_out = '%s'

print(xml_out)
json2xml.json_to_xml(params, default_settings, xml_out)
""";

string count_template =
"""
import get_metrics

instance_dir = '%s'
# '30240'
count = get_metrics.get_custom_cell_count(instance_dir)
""";

string find_min =
"""
v <- c(%s)
res <- which(v == min(v))
""";

app (file out, file err) run_model (file shfile, string executable, string param_line, string instance)
{
    "bash" shfile executable param_line emews_root instance @stdout=out @stderr=err;
}

app (void o) get_csv (file getcsv_py, string instance_dir) {
    "python" getcsv_py instance_dir;
}

app (void o) make_dir(string dirname) {
  "mkdir" "-p" dirname;
}

app (void o) make_output_dir(string instance) {
  "mkdir" "-p" (instance+"/output");
}

// deletes the specified directory
app (void o) rm_dir(string dirname) {
  "rm" "-rf" dirname;
}


main() {

  string executable = argv("exe");
  string default_xml = argv("settings");

  file model_sh = input(emews_root + "/scripts/growth_model.sh");
  file upf = input(argv("parameters"));
  file getcsv_py = input(emews_root + "/python/getcsv.py");
  trace("main");
  
  string results[];
  string upf_lines[] = file_lines(upf);

  foreach params,i in upf_lines {
    string instance_dir = "%s/instance_%i/" % (turbine_output, i+1);
    make_dir(instance_dir) => {
      make_output_dir(instance_dir) => {
        string xml_out = instance_dir + "/output/settings.xml";
        string code = to_xml_code % (params, default_xml, xml_out);
        file out <instance_dir+"out.txt">;
        file err <instance_dir+"err.txt">;
        trace("Processing instance:", i);
        python_persist(code, "'ignore'") => {
          (out,err) = run_model(model_sh, executable, xml_out, instance_dir) => {
            get_csv (getcsv_py, instance_dir);
            //  =>
            // rm_dir(instance_dir + "output/");
          }
        }
      }
    }
  }

  // string results_str = string_join(results, ",");
  // string code = find_min % results_str;
  // string mins = R(code, "toString(res)");
  // string min_idxs[] = split(mins, ",");
  // string best_params[];
  // foreach s, i in min_idxs {
    // int idx = toint(trim(s));
    // best_params[i] = upf_lines[idx - 1];
  // }
  //file best_out <turbine_output + "/output/best_parameters.txt"> =
  //  write(string_join(best_params, "\n"));
}
