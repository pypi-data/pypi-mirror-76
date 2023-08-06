#include <hdlConvertor/hdlConvertor.h>

#include <hdlConvertor/notImplementedLogger.h>

#include <hdlConvertor/vhdlConvertor/vhdlParser/vhdlLexer.h>
#include <hdlConvertor/vhdlConvertor/vhdlParser/vhdlParser.h>
#include <hdlConvertor/vhdlConvertor/designFileParser.h>

#include <hdlConvertor/svConvertor/sv2017Parser/sv2017Lexer.h>
#include <hdlConvertor/svConvertor/sv2017Parser/sv2017Parser.h>
#include <hdlConvertor/svConvertor/source_textParser.h>

#include <hdlConvertor/svConvertor/sv2017Parser/sv2017Lexer.h>
#include <hdlConvertor/svConvertor/sv2017Parser/sv2017Parser.h>
#include <hdlConvertor/svConvertor/source_textParser.h>

namespace hdlConvertor {

using namespace std;
using namespace antlr4;
using namespace antlr4::tree;
using namespace hdlConvertor::hdlAst;

bool HdlConvertor::debug = false;

class VHDLParserContainer: public iParserContainer<vhdl_antlr::vhdlLexer,
		vhdl_antlr::vhdlParser, vhdl::VhdlDesignFileParser> {
	using iParserContainer::iParserContainer;
	virtual void parseFn() override {
		vhdl_antlr::vhdlParser::Design_fileContext *tree =
				antlrParser->design_file();
		syntaxErrLogger.check_errors(); // Throw exception if errors
		hdlParser->visitDesign_file(tree);
	}
};

class SVParserContainer: public iParserContainer<sv2017_antlr::sv2017Lexer,
		sv2017_antlr::sv2017Parser, sv::Source_textParser> {
public:
	verilog_pp::VerilogPreprocContainer preproc;
	verilog_pp::FileLineMap file_line_map;

	void parse_str(std::string &input_str, bool hierarchyOnly) = delete;
	void parse_file(const filesystem::path &file_name, bool hierarchyOnly) = delete;

	SVParserContainer(hdlAst::HdlContext &context, Language _lang,
			verilog_pp::MacroDB &_defineDB) :
			iParserContainer(context, _lang, _defineDB), preproc(_lang,
					this->syntaxErrLogger, _defineDB) {
	}

	void parse_file(const filesystem::path &file_name, bool hierarchyOnly,
			std::vector<std::string> &_incdirs) {
		preproc.init(_incdirs);
		verilog_pp::VerilogPreprocOutBuffer preprocess_res(0);
		preproc.run_preproc_file(file_name, preprocess_res);
		string preprocessed_code = preprocess_res.str();
		file_line_map = preprocess_res.file_line_map;

		ANTLRInputStream input_for_parser(preprocessed_code);
		input_for_parser.name = file_name.u8string();
		this->_parse(input_for_parser, hierarchyOnly);
	}

	void parse_str(const std::string &input_str, bool hierarchyOnly,
			const std::vector<string> &_incdirs) {
		preproc.init(_incdirs);
		verilog_pp::VerilogPreprocOutBuffer preprocess_res(0);
		preproc.run_preproc_str(input_str, preprocess_res);
		string preprocessed_code = preprocess_res.str();
		file_line_map = preprocess_res.file_line_map;

		ANTLRInputStream input_for_parser(preprocessed_code);
		input_for_parser.name = STRING_FILENAME;
		this->_parse(input_for_parser, hierarchyOnly);
	}

	virtual void parseFn() override {
		lexer->language_version = lang;
		sv2017_antlr::sv2017Parser::Source_textContext *tree =
				antlrParser->source_text();
		syntaxErrLogger.check_errors(); // Throw exception if errors
		hdlParser->visitSource_text(tree);
	}
};

HdlConvertor::HdlConvertor(hdlAst::HdlContext &_c) :
		hierarchyOnly(false), c(_c) {
}

void HdlConvertor::parse(const vector<string> &_fileNames, Language lang,
		vector<string> incdir, bool _hierarchyOnly, bool _debug) {

	hierarchyOnly = _hierarchyOnly;
	debug = _debug;
	NotImplementedLogger::ENABLE = _debug;

	for (const auto &fileName : _fileNames) {
		struct stat buffer;

		if (stat(fileName.c_str(), &buffer) != 0) {
			throw ParseException(fileName + " does not exist.");
		}

		if (lang == Language::VHDL) {
			VHDLParserContainer pc(c, lang, defineDB);
			pc.parse_file(fileName, hierarchyOnly);
		} else if (lang >= Language::VERILOG1995 && lang <= Language::SV2017) {
			SVParserContainer pc(c, lang, defineDB);
			pc.parse_file(fileName, hierarchyOnly, incdir);
		} else {
			throw runtime_error("Unsupported language.");
		}
	}
}

void HdlConvertor::parse_str(const string &hdl_str, Language lang,
		vector<string> incdir, bool _hierarchyOnly, bool _debug) {
	hierarchyOnly = _hierarchyOnly;
	debug = _debug;
	NotImplementedLogger::ENABLE = _debug;

	if (lang == VHDL) {
		VHDLParserContainer pc(c, lang, defineDB);
		pc.parse_str(hdl_str, hierarchyOnly);
	} else if (lang >= Language::VERILOG1995 && lang <= Language::SV2017) {
		SVParserContainer pc(c, lang, defineDB);
		pc.parse_str(hdl_str, hierarchyOnly, incdir);
	} else {
		throw runtime_error("Unsupported language.");
	}
}

string HdlConvertor::verilog_pp(const string &fileName,
		const vector<string> _incdirs, Language lang) {
	HdlContext c; // dummy context
	SVParserContainer pc(c, lang, defineDB);
	pc.preproc.init(_incdirs);
	verilog_pp::VerilogPreprocOutBuffer res(0);
	pc.preproc.run_preproc_file(fileName, res);
	return res.str();
}

string HdlConvertor::verilog_pp_str(const string &verilog_str,
		const vector<string> _incdirs, Language lang) {
	HdlContext c; // dummy context
	SVParserContainer pc(c, lang, defineDB);
	pc.preproc.init(_incdirs);
	verilog_pp::VerilogPreprocOutBuffer res(0);
	pc.preproc.run_preproc_str(verilog_str, res);
	return res.str();
}

HdlConvertor::~HdlConvertor() {
	for (auto o : defineDB) {
		delete o.second;
	}
}
}
