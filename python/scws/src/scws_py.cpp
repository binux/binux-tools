#include <boost/python.hpp>
#include <stdlib.h>
#include <scws.h>

using namespace std;
using namespace boost::python;

struct m_scws_topword {
  string word;
  float weight;
  short times;
  char attr[2];
};

class SCWS {
  public:
    SCWS() {
      s = scws_new();
    }

    ~SCWS() {
      scws_free(s);
    }

    void set_charset(const char *cs) {
      scws_set_charset(s, cs);
    }

    int add_dict(const char *fpath, int mode) {
      return scws_add_dict(s, fpath, mode);
    }

    int set_dict(const char *fpath, int mode) {
      return scws_set_dict(s, fpath, mode);
    }

    void set_rule(const char *fpath) {
      scws_set_rule(s, fpath);
    }

    void set_ignore(int yes) {
      scws_set_ignore(s, yes);
    }

    void set_multi(int mode) {
      scws_set_multi(s, mode);
    }

    void set_duality(int yes) {
      scws_set_duality(s, yes);
    }

    void set_debug(int yes) {
      scws_set_debug(s, yes);
    }

    void send_text(const char *str, const int len) {
      scws_send_text(s, str, len);
    }

    object get_tops(int limit, char *xattr) {
      list result;
      scws_top_t res, cur;
      res = cur = scws_get_tops(s, limit, xattr);
      while (cur != NULL)
      {
        m_scws_topword tmp;
        tmp.word = cur->word;
        tmp.weight = cur->weight;
        tmp.times = cur->times;
        memcpy(tmp.attr, cur->attr, sizeof(cur->attr));

        result.append(tmp);
        cur = cur->next;
      }
      scws_free_tops(res);
      return result;
    }

    object get_result() {
      list result;
      scws_res_t res, cur;
      res = cur = scws_get_result(s);
      while (cur != NULL)
      {
        result.append(*cur);
        cur = cur->next;
      }
      scws_free_result(res);
      return result;
    }

    int has_word(char *xattr) {
      return scws_has_word(s, xattr);
    }

    object get_words(char *xattr) {
      list result;
      scws_top_t res, cur;
      res = cur = scws_get_words(s, xattr);
      while (cur != NULL)
      {
        m_scws_topword tmp;
        tmp.word = cur->word;
        tmp.weight = cur->weight;
        tmp.times = cur->times;
        memcpy(tmp.attr, cur->attr, sizeof(cur->attr));

        result.append(tmp);
        cur = cur->next;
      }
      scws_free_tops(res);
      return result;
    }

  private:
    scws_t s;
};

struct attr_to_python_str {
  static PyObject* convert(char * a) {
    return PyString_FromString(a);
  }
};

BOOST_PYTHON_MODULE(scws_py) {
  class_<SCWS>("SCWS")
    .def("set_charset", &SCWS::set_charset)
    .def("add_dict", &SCWS::add_dict)
    .def("set_dict", &SCWS::set_dict)
    .def("set_rule", &SCWS::set_rule)
    .def("set_ignore", &SCWS::set_ignore)
    .def("set_multi", &SCWS::set_multi)
    .def("set_duality", &SCWS::set_duality)
    .def("set_debug", &SCWS::set_debug)
    .def("send_text", &SCWS::send_text)
    .def("get_result", &SCWS::get_result)
    .def("get_tops", &SCWS::get_tops)
    .def("has_word", &SCWS::has_word)
    .def("get_words", &SCWS::get_words);

  class_<scws_result>("result")
    .def_readonly("off", &scws_result::off)
    .def_readonly("idf", &scws_result::idf)
    .def_readonly("len", &scws_result::len)
    .def_readonly("attr", &scws_result::attr);
  to_python_converter<char [3], attr_to_python_str>();

  class_<m_scws_topword>("topword")
    .def_readonly("word", &m_scws_topword::word)
    .def_readonly("weight", &m_scws_topword::weight)
    .def_readonly("times", &m_scws_topword::times)
    .def_readonly("attr", &m_scws_topword::attr);
  to_python_converter<char [2], attr_to_python_str>();

  scope().attr("SCWS_XDICT_TXT") = SCWS_XDICT_TXT;
  scope().attr("SCWS_XDICT_XDB") = SCWS_XDICT_XDB;
  scope().attr("SCWS_XDICT_MEM") = SCWS_XDICT_MEM;

  scope().attr("SCWS_MULTI_NONE") = SCWS_MULTI_NONE;
  scope().attr("SCWS_MULTI_SHORT") = SCWS_MULTI_SHORT;
  scope().attr("SCWS_MULTI_DUALITY") = SCWS_MULTI_DUALITY;
  scope().attr("SCWS_MULTI_ZMAIN") = SCWS_MULTI_ZMAIN;
  scope().attr("SCWS_MULTI_ZALL") = SCWS_MULTI_ZALL;
}
