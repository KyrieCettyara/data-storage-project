--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.address (
    address_id integer NOT NULL,
    street_number character varying(10),
    street_name character varying(200),
    city character varying(100),
    cd integer
);


ALTER TABLE public.address OWNER TO postgres;

--
-- Name: address_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.address_status (
    status_id integer NOT NULL,
    address_status character varying(30)
);


ALTER TABLE public.address_status OWNER TO postgres;

--
-- Name: author; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.author (
    author_id integer NOT NULL,
    author_name character varying(400)
);


ALTER TABLE public.author OWNER TO postgres;

--
-- Name: book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book (
    book_id integer NOT NULL,
    title character varying(400),
    isbn13 character varying(13),
    language_id integer,
    num_pages integer,
    publication_date date,
    publisher_id integer
);


ALTER TABLE public.book OWNER TO postgres;

--
-- Name: book_author; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_author (
    book_id integer NOT NULL,
    author_id integer NOT NULL
);


ALTER TABLE public.book_author OWNER TO postgres;

--
-- Name: book_language; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_language (
    language_id integer NOT NULL,
    language_code character varying(8),
    language_name character varying(50)
);


ALTER TABLE public.book_language OWNER TO postgres;

--
-- Name: country; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.country (
    country_id integer NOT NULL,
    country_name character varying(200)
);


ALTER TABLE public.country OWNER TO postgres;

--
-- Name: cust_order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cust_order (
    order_id integer NOT NULL,
    order_date timestamp without time zone,
    customer_id integer,
    shipping_method_id integer,
    dest_address_id integer
);


ALTER TABLE public.cust_order OWNER TO postgres;

--
-- Name: cust_order_order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cust_order_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cust_order_order_id_seq OWNER TO postgres;

--
-- Name: cust_order_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cust_order_order_id_seq OWNED BY public.cust_order.order_id;


--
-- Name: customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer (
    customer_id integer NOT NULL,
    first_name character varying(200),
    last_name character varying(200),
    email character varying(350)
);


ALTER TABLE public.customer OWNER TO postgres;

--
-- Name: customer_address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer_address (
    customer_id integer NOT NULL,
    address_id integer NOT NULL,
    status_id integer
);


ALTER TABLE public.customer_address OWNER TO postgres;

--
-- Name: order_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_history (
    history_id integer NOT NULL,
    order_id integer,
    status_id integer,
    status_date timestamp without time zone
);


ALTER TABLE public.order_history OWNER TO postgres;

--
-- Name: order_history_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_history_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_history_history_id_seq OWNER TO postgres;

--
-- Name: order_history_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_history_history_id_seq OWNED BY public.order_history.history_id;


--
-- Name: order_line; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_line (
    line_id integer NOT NULL,
    order_id integer,
    book_id integer,
    price numeric(5,2)
);


ALTER TABLE public.order_line OWNER TO postgres;

--
-- Name: order_line_line_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_line_line_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_line_line_id_seq OWNER TO postgres;

--
-- Name: order_line_line_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_line_line_id_seq OWNED BY public.order_line.line_id;


--
-- Name: order_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_status (
    status_id integer NOT NULL,
    status_value character varying(20)
);


ALTER TABLE public.order_status OWNER TO postgres;

--
-- Name: publisher; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publisher (
    publisher_id integer NOT NULL,
    publisher_name character varying(400)
);


ALTER TABLE public.publisher OWNER TO postgres;

--
-- Name: shipping_method; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shipping_method (
    method_id integer NOT NULL,
    method_name character varying(100),
    cost numeric(6,2)
);



