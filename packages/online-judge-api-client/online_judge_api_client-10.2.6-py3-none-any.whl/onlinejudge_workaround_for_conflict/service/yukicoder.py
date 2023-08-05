# Python Version: 3.x
# -*- coding: utf-8 -*-
"""
the module for yukicoder (https://yukicoder.me/)

:note: There is the official API https://petstore.swagger.io/?url=https://yukicoder.me/api/swagger.yaml
"""

import posixpath
import urllib.parse
from typing import *

import bs4

import onlinejudge_workaround_for_conflict._implementation.logging as log
import onlinejudge_workaround_for_conflict._implementation.testcase_zipper
import onlinejudge_workaround_for_conflict._implementation.utils as utils
import onlinejudge_workaround_for_conflict.dispatch
from onlinejudge_workaround_for_conflict.type import *


class YukicoderService(onlinejudge_workaround_for_conflict.type.Service):
    def get_url_of_login_page(self):
        return self.get_url()

    def is_logged_in(self, *, session: Optional[requests.Session] = None) -> bool:
        session = session or utils.get_default_session()
        url = 'https://yukicoder.me'
        resp = utils.request('GET', url, session=session)
        assert resp.status_code == 200
        return 'login-btn' not in str(resp.content)

    def get_url(self) -> str:
        return 'https://yukicoder.me/'

    def get_name(self) -> str:
        return 'yukicoder'

    @classmethod
    def from_url(cls, url: str) -> Optional['YukicoderService']:
        # example: http://yukicoder.me/
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'yukicoder.me':
            return cls()
        return None

    # example: https://yukicoder.me/submissions?page=4220
    # example: https://yukicoder.me/submissions?page=2192&status=AC
    # NOTE: 1ページしか読まない 全部欲しい場合は呼び出し側で頑張る
    def get_submissions(self, *, page: int, status: Optional[str] = None, session: Optional[requests.Session] = None) -> List[Any]:
        """
        .. deprecated:: 6.0.0
            This method may be deleted in future.
        """
        assert isinstance(page, int) and page >= 1
        url = 'https://yukicoder.me/submissions?page=%d' % page
        if status is not None:
            assert status in 'AC WA RE TLE MLE OLE J_TLE CE WJ Judge NoOut IE'.split()
            url += '&status=' + status
        columns, rows = self._get_and_parse_the_table(url, session=session)
        assert columns == ['#', '提出日時', '', '提出者', '問題', '言語', '結果', '実行時間', 'コード長']  # 空白は「このユーザーの提出の表示」の虫眼鏡のため
        for row in rows:
            for column in columns:
                if column and row[column].find('a'):
                    row[column + '/url'] = row[column].find('a').attrs.get('href')
                if column == '#':
                    row[column] = int(row[column].text)
                elif column == '':
                    del row[column]
                else:
                    row[column] = row[column].text.strip()
        return rows

    # example: https://yukicoder.me/problems?page=2
    # NOTE: loginしてると
    def get_problems(self, *, page: int, comp_problem: bool = True, other: bool = False, sort: Optional[str] = None, session: Optional[requests.Session] = None) -> List[Any]:
        """
        .. deprecated:: 6.0.0
            This method may be deleted in future.
        """
        assert isinstance(page, int) and page >= 1
        url = 'https://yukicoder.me/problems'
        if other:
            url += '/other'
        url += '?page=%d' % page
        if comp_problem:  # 未完成問題は(ログインしてても)デフォルトで除外
            url += '&comp_problem=on'
        if sort is not None:
            assert sort in (
                'no_asc',
                'level_asc',
                'level_desc',
                'solved_asc',
                'solved_desc',
                'fav_asc',
                'fav_desc',
            )
            url += '&sort=' + sort
        columns, rows = self._get_and_parse_the_table(url, session=session)
        assert columns == ['ナンバー', '問題名', 'レベル', 'タグ', '作問者', '解いた人数', 'Fav']
        for row in rows:
            for column in columns:
                if column and row[column].find('a'):
                    row[column + '/url'] = row[column].find('a').attrs.get('href')
                if column in ('ナンバー', '解いた人数', 'Fav'):
                    row[column] = int(row[column].text)
                elif column == 'レベル':
                    row[column] = self._parse_star(row[column])
                elif column == 'タグ':
                    # NOTE: ログインしてないとタグが非表示の仕様
                    # NOTE: ログインしてるはずだけどrequestsからGETしてもタグが降ってこない場合は適切な Session objectを指定してるか確認
                    row[column] = row[column].text.strip().split()
                else:
                    row[column] = row[column].text.strip()
        return rows

    def _get_and_parse_the_table(self, url: str, *, session: Optional[requests.Session] = None) -> Tuple[List[Any], List[Dict[str, bs4.Tag]]]:
        # get
        session = session or utils.get_default_session()
        resp = utils.request('GET', url, session=session)
        # parse
        soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.html_parser)
        assert len(soup.find_all('table')) == 1
        table = soup.find('table')
        columns = [th.text.strip() for th in table.find('thead').find('tr') if th.name == 'th']
        data = []  # type: List[Dict[str, List[str]]]
        for row in table.find('tbody').find_all('tr'):
            values = [td for td in row if td.name == 'td']
            assert len(columns) == len(values)
            data += [dict(zip(columns, values))]
        return columns, data

    def _parse_star(self, tag: bs4.Tag) -> str:
        star = str(len(tag.find_all(class_='fa-star')))
        if tag.find_all(class_='fa-star-half-full'):
            star += '.5'
        return star


class YukicoderProblem(onlinejudge_workaround_for_conflict.type.Problem):
    def __init__(self, *, problem_no=None, problem_id=None):
        assert problem_no or problem_id
        assert not problem_no or isinstance(problem_no, int)
        assert not problem_id or isinstance(problem_id, int)
        self.problem_no = problem_no
        self.problem_id = problem_id

    def download_sample_cases(self, *, session: Optional[requests.Session] = None) -> List[TestCase]:
        session = session or utils.get_default_session()
        # get
        resp = utils.request('GET', self.get_url(), session=session)
        # parse
        soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.html_parser)
        samples = onlinejudge_workaround_for_conflict._implementation.testcase_zipper.SampleZipper()
        for pre in soup.select('.sample pre'):
            log.debug('pre: %s', str(pre))
            it = self._parse_sample_tag(pre)
            if it is not None:
                data, name = it
                samples.add(data.encode(), name)
        return samples.get()

    def download_system_cases(self, *, session: Optional[requests.Session] = None) -> List[TestCase]:
        """
        :raises NotLoggedInError:
        """

        session = session or utils.get_default_session()
        if not self.get_service().is_logged_in(session=session):
            raise NotLoggedInError
        url = '{}/testcase.zip'.format(self.get_url())
        resp = utils.request('GET', url, session=session)
        fmt = 'test_%e/%s'
        return onlinejudge_workaround_for_conflict._implementation.testcase_zipper.extract_from_zip(resp.content, fmt)

    def _parse_sample_tag(self, tag: bs4.Tag) -> Optional[Tuple[str, str]]:
        assert isinstance(tag, bs4.Tag)
        assert tag.name == 'pre'
        prv = utils.previous_sibling_tag(tag)
        pprv = tag.parent and utils.previous_sibling_tag(tag.parent)
        if prv.name == 'h6' and tag.parent.name == 'div' and tag.parent['class'] == ['paragraph'] and pprv.name == 'h5':
            log.debug('h6: %s', str(prv))
            log.debug('name.encode(): %s', prv.string.encode())

            s = utils.parse_content(tag)

            return utils.textfile(s.lstrip()), pprv.string + ' ' + prv.string
        return None

    def submit_code(self, code: bytes, language_id: LanguageId, *, filename: Optional[str] = None, session: Optional[requests.Session] = None) -> onlinejudge_workaround_for_conflict.type.Submission:
        """
        :raises NotLoggedInError:
        """

        session = session or utils.get_default_session()
        # get
        url = self.get_url() + '/submit'
        resp = utils.request('GET', url, session=session)
        # parse
        soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.html_parser)
        form = soup.find('form', id='submit_form')
        if not form:
            log.error('form not found')
            raise NotLoggedInError
        # post
        form = utils.FormSender(form, url=resp.url)
        form.set('lang', language_id)
        form.set_file('file', filename or 'code', code)
        form.unset('custom_test')
        resp = form.request(session=session)
        resp.raise_for_status()
        # result
        if 'submissions' in resp.url:
            # example: https://yukicoder.me/submissions/314087
            log.success('success: result: %s', resp.url)
            return utils.DummySubmission(resp.url, problem=self)
        else:
            log.failure('failure')
            soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.html_parser)
            for div in soup.findAll('div', attrs={'role': 'alert'}):
                log.warning('yukicoder says: "%s"', div.string)
            raise SubmissionError

    def get_available_languages(self, *, session: Optional[requests.Session] = None) -> List[Language]:
        session = session or utils.get_default_session()
        # get
        # We use the problem page since it is available without logging in
        resp = utils.request('GET', self.get_url(), session=session)
        # parse
        soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.html_parser)
        select = soup.find('select', id='lang')
        languages = []  # type: List[Language]
        for option in select.find_all('option'):
            languages += [Language(option.attrs['value'], ' '.join(option.string.split()))]
        return languages

    def get_url(self) -> str:
        if self.problem_no:
            return 'https://yukicoder.me/problems/no/{}'.format(self.problem_no)
        elif self.problem_id:
            return 'https://yukicoder.me/problems/{}'.format(self.problem_id)
        else:
            raise ValueError

    @classmethod
    def from_url(cls, url: str) -> Optional['YukicoderProblem']:
        # example: https://yukicoder.me/problems/no/499
        # example: http://yukicoder.me/problems/1476
        result = urllib.parse.urlparse(url)
        dirname, basename = posixpath.split(utils.normpath(result.path))
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'yukicoder.me':
            n = None  # type: Optional[int]
            try:
                n = int(basename)
            except ValueError:
                pass
            if n is not None:
                if dirname == '/problems/no':
                    return cls(problem_no=n)
                if dirname == '/problems':
                    return cls(problem_id=n)
        return None

    def get_service(self) -> YukicoderService:
        return YukicoderService()

    def get_input_format(self, *, session: Optional[requests.Session] = None) -> Optional[str]:
        session = session or utils.get_default_session()
        # get
        resp = utils.request('GET', self.get_url(), session=session)
        # parse
        soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.html_parser)
        for h4 in soup.find_all('h4'):
            if h4.string == '入力':
                return h4.parent.find('pre').decode_contents(formatter=None)
        return None


onlinejudge_workaround_for_conflict.dispatch.services += [YukicoderService]
onlinejudge_workaround_for_conflict.dispatch.problems += [YukicoderProblem]
