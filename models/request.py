from math import sqrt


class Request(object):

    def __init__(self, raw_request):
        self.raw_request = raw_request

    def return_results(self, index, *args, **kwargs):
        self.parse_request(index)
        return self.find_results(index, *args, **kwargs)

    def parse_request(self, index):
        """
        Parse the raw request given at object's creation.
        """
        raise NotImplementedError

    def find_results(self, index):
        """
        Implements here the algorithm to find results.
        """
        raise NotImplementedError


class BooleanRequest(Request):
    pass


class VectorialRequest(Request):

    def parse_request(self, index):
        """
        We parse the raw request by splitting on space.
        """
        self.parsed_request = [
            elt.lower() for elt in self.raw_request.split(' ') if elt.lower() in index.keys()
        ]

    def find_results(self, index, weight_function=lambda doc_len, tf, df: 1 * tf * df):
        """
        Apply algorithm to find results from index.
        + params:
            - index: ReverseIndex object where we look for results
            - weight_function: function which calculate weight of given term
        + return:
            {document_id: score}
        + summary:
            Given N documents with normalized factors ndj and a request q = (t1,q, ..., t1,K)
            The pseudo-code of the algorithm is described here (p. 196 in 1st lecture):
                nq = 0
                for j in [1, ..., N] do
                    s[j] = 0
                    n[j] = 0
                for i in [1, ..., K] do
                    w_ti,q_q = ndq * p_tfi,q_q * p_df_ti,q
                    nq = nq + (w_ti,q_q) ** 2
                    L = posting list of ti,q
                    for dj in L do
                        w_ti,q_dj = ndj * p_tfi,q_dj * p_df_ti,q
                        n[j] = n[j] + (w_ti,q_dj) ** 2
                        s[j] = s[j] + (w_ti,q_dj * w_ti,q_q)
                for j in [1, ..., N] do
                    if s[j] != 0 then
                        s[j] = s[j] / (sqrt(n[j]) * sqrt(nq))
                return document_id list sorted by decreasing scores
        """
        nq = 0
        ndj = {
            posting_id: 0
            for token in self.parsed_request
            for posting_id, _, _ in index[token][1]
        }
        s = {
            posting_id: 0
            for token in self.parsed_request
            for posting_id, _, _ in index[token][1]
        }
        for token in self.parsed_request:
            wq = weight_function(doc_len=len(self.parsed_request), tf=1, df=index[token][0])
            nq += wq ** 2
            for posting_id, doc_frequence, doc_len in index[token][1]:
                wj = weight_function(doc_len=doc_len, tf=doc_frequence, df=index[token][0])
                ndj[posting_id] += wj ** 2
                s[posting_id] += wq * wj
        s = {key: value / (sqrt(nq) * sqrt(ndj[key])) for key, value in s.items()}
        return [doc_id for doc_id, _ in sorted(s.items(), key=lambda x: x[1], reverse=True)]
